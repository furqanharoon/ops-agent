"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

interface FieldResult {
  expected: unknown;
  actual: unknown;
  passed: boolean;
}

interface EvalResult {
  id: number;
  name: string;
  query: string;
  passed: boolean;
  comparison: Record<string, FieldResult>;
}

interface EvalRunResponse {
  total: number;
  passed: number;
  pass_rate: number;
  results: EvalResult[];
}

export default function EvaluationsPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<EvalRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleRunEvals() {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const { data: { job_id } } = await api.post<{ job_id: string }>("/evals/run");

      // Poll until done
      while (true) {
        await new Promise((r) => setTimeout(r, 3000));
        const { data: job } = await api.get<{ status: string; result: EvalRunResponse | string }>(`/evals/result/${job_id}`);

        if (job.status === "done") {
          setData(job.result as EvalRunResponse);
          break;
        }
        if (job.status === "error") {
          setError(typeof job.result === "string" ? job.result : "Eval run failed.");
          break;
        }
        // status === "running" — keep polling
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Eval run failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Evaluations</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Run the test suite against all eval cases in investigations.json
          </p>
        </div>
        <Button onClick={handleRunEvals} disabled={loading}>
          {loading ? "Running…" : "Run Evals"}
        </Button>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6 text-sm text-destructive">{error}</CardContent>
        </Card>
      )}

      {loading && (
        <Card>
          <CardContent className="pt-6 text-sm text-muted-foreground">
            Running evaluations — this may take a few minutes…
          </CardContent>
        </Card>
      )}

      {data && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Summary</CardTitle>
              <CardDescription>
                {data.passed}/{data.total} cases passed ({data.pass_rate}% pass rate)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-3">
                <Badge variant={data.passed === data.total ? "default" : "destructive"}>
                  {data.passed} Passed
                </Badge>
                <Badge variant="secondary">{data.total - data.passed} Failed</Badge>
              </div>
            </CardContent>
          </Card>

          {data.results.map((result) => (
            <Card key={result.id} className={result.passed ? "border-green-500/40" : "border-destructive/40"}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-base">{result.query}</CardTitle>
                    <CardDescription className="mt-0.5">{result.name}</CardDescription>
                  </div>
                  <Badge variant={result.passed ? "default" : "destructive"}>
                    {result.passed ? "Pass" : "Fail"}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-muted-foreground text-xs border-b">
                      <th className="text-left pb-2 font-medium">Field</th>
                      <th className="text-left pb-2 font-medium">Expected</th>
                      <th className="text-left pb-2 font-medium">Actual</th>
                      <th className="text-left pb-2 font-medium">Result</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(result.comparison).map(([field, value]) => (
                      <tr key={field} className="border-b last:border-0">
                        <td className="py-2 font-mono text-xs text-muted-foreground">{field}</td>
                        <td className="py-2">{String(value.expected)}</td>
                        <td className="py-2">{String(value.actual)}</td>
                        <td className="py-2">
                          <Badge variant={value.passed ? "default" : "destructive"} className="text-xs">
                            {value.passed ? "✓" : "✗"}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </CardContent>
            </Card>
          ))}
        </>
      )}

      {!loading && !data && !error && (
        <Card>
          <CardContent className="pt-6 text-sm text-muted-foreground">
            Click <strong>Run Evals</strong> to execute all test cases.
          </CardContent>
        </Card>
      )}
    </div>
  );
}
