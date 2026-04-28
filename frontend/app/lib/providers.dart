import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'features/shared/models/incident_model.dart';
import 'features/shared/models/staff_model.dart';
import 'features/shared/models/guest_model.dart';
import 'core/constants/app_constants.dart';

// ── Session Provider ──
final sharedPreferencesProvider = Provider<SharedPreferences>((ref) {
  throw UnimplementedError('Must be overridden in main');
});

// ── User Type Provider ──
class UserTypeNotifier extends Notifier<String?> {
  @override
  String? build() {
    final prefs = ref.read(sharedPreferencesProvider);
    return prefs.getString(AppConstants.userTypeKey);
  }

  void set(String? value) {
    state = value;
  }

  Future<void> logout() async {
    final prefs = ref.read(sharedPreferencesProvider);
    await prefs.remove(AppConstants.userTypeKey);
    state = null;
  }
}

final userTypeProvider = NotifierProvider<UserTypeNotifier, String?>(
  UserTypeNotifier.new,
);

// ── Active Incident Provider ──
class ActiveIncidentNotifier extends Notifier<bool> {
  @override
  bool build() => true;

  void setActive(bool value) => state = value;
}

final activeIncidentProvider = NotifierProvider<ActiveIncidentNotifier, bool>(
  ActiveIncidentNotifier.new,
);

// ── Mock Data ──
const mockStaff = StaffModel(
  id: 'EMP-2041',
  name: 'Rajesh Kumar',
  role: StaffRole.security,
  floor: 'Floor 3',
  zone: 'Wing B',
  hotel: 'Taj Lands End, Mumbai',
  shiftStart: '06:00 AM',
  shiftEnd: '08:00 PM',
);

const mockGuest = GuestModel(
  name: 'Sarah',
  room: '402',
  wing: 'North Wing',
  floor: 'Floor 4',
  hotel: 'The Grand Hotel',
  checkOut: '2026-04-26',
);

final mockIncident = IncidentModel(
  id: 'INC-001',
  type: IncidentType.medical,
  location: 'Sector 4, Main Concourse',
  detail: 'Subject unresponsive. EMS dispatched.',
  severity: IncidentSeverity.critical,
  status: IncidentStatus.active,
  startTime: DateTime(2026, 4, 25, 14, 02),
  responders: const [
    ResponderModel(id: 'R1', name: 'Unit 4 - Alpha', role: 'First Responder', eta: '2 mins', status: 'En route'),
    ResponderModel(id: 'R2', name: 'EMS Ground', role: 'Medical', eta: '5 mins', status: 'Dispatched'),
    ResponderModel(id: 'R3', name: 'Security Team B', role: 'Security', eta: 'On Scene', status: 'On Scene'),
  ],
  sopSteps: const [
    SOPStep(num: 1, text: 'Secure immediate area', done: true, completedAt: '14:02'),
    SOPStep(num: 2, text: 'Dispatch EMS', done: true, completedAt: '14:03'),
    SOPStep(num: 3, text: 'Clear path for EMS', done: false, isActive: true),
    SOPStep(num: 4, text: 'Notify family/emergency contact', done: false),
    SOPStep(num: 5, text: 'File incident report', done: false),
  ],
);
