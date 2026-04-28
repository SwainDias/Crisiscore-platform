import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/role_badge.dart';

class StaffAccountTabScreen extends ConsumerWidget {
  const StaffAccountTabScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
          children: [
            Text(
              'Account',
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w800, color: AppColors.onSurface),
            ),
            const SizedBox(height: 24),
            
            // Profile Info Card
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppColors.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(24),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.onSurface.withValues(alpha: 0.05),
                    blurRadius: 40,
                    offset: const Offset(0, 10),
                  ),
                ],
              ),
              child: Column(
                children: [
                  Stack(
                    children: [
                      CircleAvatar(
                        radius: 50,
                        backgroundColor: AppColors.primaryContainer.withValues(alpha: 0.2),
                        child: const Icon(Icons.person, size: 50, color: AppColors.primary),
                      ),
                      Positioned(
                        bottom: 0,
                        right: 0,
                        child: Container(
                          padding: const EdgeInsets.all(4),
                          decoration: const BoxDecoration(
                            color: AppColors.primary,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.edit, size: 16, color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    mockStaff.name,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 8),
                  RoleBadge(label: mockStaff.role.name.toUpperCase()),
                  const SizedBox(height: 8),
                  Text(
                    mockStaff.hotel,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Assignment Details
            _StaffAccountTile(
              icon: Icons.badge_outlined,
              title: 'Employee ID',
              value: mockStaff.id,
            ),
            const SizedBox(height: 12),
            _StaffAccountTile(
              icon: Icons.location_on_outlined,
              title: 'Assigned Zone',
              value: '${mockStaff.floor}, ${mockStaff.zone}',
            ),
            const SizedBox(height: 12),
            _StaffAccountTile(
              icon: Icons.schedule_outlined,
              title: 'Shift Schedule',
              value: '${mockStaff.shiftStart} - ${mockStaff.shiftEnd}',
            ),
            
            const SizedBox(height: 32),
            
            // Logout Card
            Container(
              decoration: BoxDecoration(
                color: AppColors.errorContainer.withValues(alpha: 0.2),
                borderRadius: BorderRadius.circular(24),
              ),
              child: ListTile(
                onTap: () async {
                  await ref.read(userTypeProvider.notifier).logout();
                  if (context.mounted) {
                    context.go('/onboarding');
                  }
                },
                leading: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: const BoxDecoration(
                    color: AppColors.errorContainer,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.logout, color: AppColors.error, size: 20),
                ),
                title: const Text(
                  'Logout',
                  style: TextStyle(color: AppColors.error, fontWeight: FontWeight.w700),
                ),
                subtitle: const Text('End duty and exit session'),
                trailing: const Icon(Icons.chevron_right, color: AppColors.error),
              ),
            ),
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }
}

class _StaffAccountTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;

  const _StaffAccountTile({
    required this.icon,
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppColors.primaryContainer.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: AppColors.primary, size: 20),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(color: AppColors.onSurfaceVariant),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
