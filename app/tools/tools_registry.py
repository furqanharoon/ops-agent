from app.tools.incident_tools import(get_incident, get_incident_duration, get_incident_timeline)

tools_registry={
  "get_incident": get_incident,
  "get_incident_duration": get_incident_duration,
  "get_incident_timeline": get_incident_timeline,
}
