enum IncidentType { fire, medical, security, weather, flooding }
enum IncidentSeverity { low, moderate, high, critical }
enum IncidentStatus { active, resolved, pending }

class ResponderModel {
  final String id;
  final String name;
  final String role;
  final String eta;
  final String status;

  const ResponderModel({
    required this.id,
    required this.name,
    required this.role,
    required this.eta,
    required this.status,
  });
}

class SOPStep {
  final int num;
  final String text;
  final bool done;
  final bool isActive;
  final String? completedAt;

  const SOPStep({
    required this.num,
    required this.text,
    this.done = false,
    this.isActive = false,
    this.completedAt,
  });
}

class IncidentModel {
  final String id;
  final IncidentType type;
  final String location;
  final String detail;
  final IncidentSeverity severity;
  final IncidentStatus status;
  final DateTime startTime;
  final List<ResponderModel> responders;
  final List<SOPStep> sopSteps;

  const IncidentModel({
    required this.id,
    required this.type,
    required this.location,
    required this.detail,
    required this.severity,
    required this.status,
    required this.startTime,
    this.responders = const [],
    this.sopSteps = const [],
  });
}
