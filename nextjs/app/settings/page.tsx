import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-6xl">
      <Card>
        <CardHeader>
          <CardTitle>Settings</CardTitle>
          <CardDescription>Frontend runtime configuration.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>
            <span className="text-muted-foreground">API base URL: </span>
            {process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
