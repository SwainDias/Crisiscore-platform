import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/constants/app_constants.dart';
import '../../providers.dart';
import '../../features/auth/screens/splash_screen.dart';
import '../../features/auth/screens/onboarding_screen.dart';
import '../../features/auth/screens/staff_login_screen.dart';
import '../../features/auth/screens/role_confirmation_screen.dart';
import '../../features/auth/screens/guest_checkin_screen.dart';

import '../../features/staff/screens/staff_shell_screen.dart';
import '../../features/staff/screens/staff_home_screen.dart';
import '../../features/staff/screens/staff_map_tab_screen.dart';
import '../../features/staff/screens/staff_alerts_tab_screen.dart';
import '../../features/staff/screens/staff_guide_tab_screen.dart';
import '../../features/staff/screens/crisis_trigger_screen.dart';
import '../../features/staff/screens/active_incident_screen.dart';
import '../../features/staff/screens/post_incident_screen.dart';
import '../../features/staff/screens/silent_panic_screen.dart';
import '../../features/staff/screens/training_drill_screen.dart';

import '../../features/guest/screens/guest_shell_screen.dart';
import '../../features/guest/screens/guest_home_screen.dart';
import '../../features/guest/screens/guest_alerts_tab_screen.dart';
import '../../features/guest/screens/guest_guide_tab_screen.dart';
import '../../features/guest/screens/guest_account_tab_screen.dart';
import '../../features/guest/screens/guest_instructions_screen.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _staffHomeBranchKey = GlobalKey<NavigatorState>();
final _staffMapBranchKey = GlobalKey<NavigatorState>();
final _staffAlertsBranchKey = GlobalKey<NavigatorState>();
final _staffGuideBranchKey = GlobalKey<NavigatorState>();

final _guestHomeBranchKey = GlobalKey<NavigatorState>();
final _guestAlertsBranchKey = GlobalKey<NavigatorState>();
final _guestGuideBranchKey = GlobalKey<NavigatorState>();
final _guestAccountBranchKey = GlobalKey<NavigatorState>();

const _authRoutes = <String>{
  '/onboarding',
  '/staff/login',
  '/staff/role-confirm',
  '/guest/checkin',
};

final appRouterProvider = Provider<GoRouter>((ref) {
  final userType = ref.watch(userTypeProvider);

  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: '/splash',
    redirect: (context, state) {
      final location = state.uri.path;
      final isStaffRoute = location.startsWith('/staff/');
      final isGuestRoute = location.startsWith('/guest/');
      final isAuthRoute = _authRoutes.contains(location);

      if (location == '/') {
        return '/splash';
      }

      if (location == '/splash') {
        return null;
      }

      if (userType == null) {
        if (isStaffRoute || isGuestRoute) {
          return '/onboarding';
        }
        return null;
      }

      if (userType == AppConstants.staffType) {
        if (isGuestRoute) {
          return '/staff/home';
        }
        if (location == '/onboarding' || location == '/guest/checkin') {
          return '/staff/home';
        }
        return null;
      }

      if (userType == AppConstants.guestType) {
        if (isStaffRoute) {
          return '/guest/home';
        }
        if (isAuthRoute) {
          return '/guest/home';
        }
        return null;
      }

      return null;
    },
    routes: [
      // Root redirect
      GoRoute(
        path: '/',
        redirect: (context, state) => '/splash',
      ),

      // Auth flow
      GoRoute(
        path: '/splash',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: '/onboarding',
        builder: (context, state) => const OnboardingScreen(),
      ),
      GoRoute(
        path: '/staff/login',
        builder: (context, state) => const StaffLoginScreen(),
      ),
      GoRoute(
        path: '/staff/role-confirm',
        builder: (context, state) => const RoleConfirmationScreen(),
      ),
      GoRoute(
        path: '/guest/checkin',
        builder: (context, state) => const GuestCheckinScreen(),
      ),

      // Staff shell (state preserved across tabs)
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) =>
            StaffShellScreen(navigationShell: navigationShell),
        branches: [
          StatefulShellBranch(
            navigatorKey: _staffHomeBranchKey,
            routes: [
              GoRoute(
                path: '/staff/home',
                builder: (context, state) => const StaffHomeScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _staffMapBranchKey,
            routes: [
              GoRoute(
                path: '/staff/map',
                builder: (context, state) => const StaffMapTabScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _staffAlertsBranchKey,
            routes: [
              GoRoute(
                path: '/staff/alerts',
                builder: (context, state) => const StaffAlertsTabScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _staffGuideBranchKey,
            routes: [
              GoRoute(
                path: '/staff/guide',
                builder: (context, state) => const StaffGuideTabScreen(),
              ),
            ],
          ),
        ],
      ),

      // Staff full-screen routes (outside shell)
      GoRoute(
        path: '/staff/trigger',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) => const CrisisTriggerScreen(),
      ),
      GoRoute(
        path: '/staff/incident/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) =>
            ActiveIncidentScreen(incidentId: state.pathParameters['id'] ?? ''),
      ),
      GoRoute(
        path: '/staff/post-incident/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) =>
            PostIncidentScreen(incidentId: state.pathParameters['id'] ?? ''),
      ),
      GoRoute(
        path: '/staff/drill/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) =>
            TrainingDrillScreen(drillId: state.pathParameters['id'] ?? '1'),
      ),
      GoRoute(
        path: '/staff/silent-panic',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) => const SilentPanicScreen(),
      ),

      // Guest shell (state preserved across tabs)
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) =>
            GuestShellScreen(navigationShell: navigationShell),
        branches: [
          StatefulShellBranch(
            navigatorKey: _guestHomeBranchKey,
            routes: [
              GoRoute(
                path: '/guest/home',
                builder: (context, state) => const GuestHomeScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _guestAlertsBranchKey,
            routes: [
              GoRoute(
                path: '/guest/alerts',
                builder: (context, state) => const GuestAlertsTabScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _guestGuideBranchKey,
            routes: [
              GoRoute(
                path: '/guest/guide',
                builder: (context, state) => const GuestGuideTabScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _guestAccountBranchKey,
            routes: [
              GoRoute(
                path: '/guest/account',
                builder: (context, state) => const GuestAccountTabScreen(),
              ),
            ],
          ),
        ],
      ),

      // Guest full-screen routes (outside shell)
      GoRoute(
        path: '/guest/instructions',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) => const GuestInstructionsScreen(),
      ),
    ],
  );
});
