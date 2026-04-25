enum StaffRole { security, medical, management, maintenance }

class StaffModel {
  final String id;
  final String name;
  final StaffRole role;
  final String floor;
  final String zone;
  final String hotel;
  final String shiftStart;
  final String shiftEnd;

  const StaffModel({
    required this.id,
    required this.name,
    required this.role,
    required this.floor,
    required this.zone,
    required this.hotel,
    required this.shiftStart,
    required this.shiftEnd,
  });

  String get roleName {
    switch (role) {
      case StaffRole.security:
        return 'Security Officer';
      case StaffRole.medical:
        return 'Medical Staff';
      case StaffRole.management:
        return 'Management';
      case StaffRole.maintenance:
        return 'Maintenance';
    }
  }
}
