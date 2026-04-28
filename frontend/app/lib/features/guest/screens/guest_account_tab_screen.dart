import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';

class GuestAccountTabScreen extends ConsumerWidget {
  const GuestAccountTabScreen({super.key});

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
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(24),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.onSurface.withValues(alpha: 0.05),
                    blurRadius: 20,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 40,
                    backgroundColor: AppColors.primaryContainer.withValues(alpha: 0.2),
                    child: const Icon(Icons.person, size: 40, color: AppColors.primary),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    mockGuest.name,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Guest • Room ${mockGuest.room}',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Stay Details Card
            _AccountActionTile(
              icon: Icons.hotel_outlined,
              title: mockGuest.hotel,
              subtitle: '${mockGuest.wing}, ${mockGuest.floor}',
              onTap: () {},
            ),
            
            const SizedBox(height: 12),
            
            _AccountActionTile(
              icon: Icons.notifications_outlined,
              title: 'Notification Settings',
              subtitle: 'Emergency alerts and sound',
              onTap: () {},
            ),
            
            const SizedBox(height: 12),
            
            _AccountActionTile(
              icon: Icons.help_outline,
              title: 'Support',
              subtitle: 'Contact hotel security or assistance',
              onTap: () {},
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
                subtitle: const Text('End current session and exit'),
                trailing: const Icon(Icons.chevron_right, color: AppColors.error),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _AccountActionTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _AccountActionTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(24),
      ),
      child: ListTile(
        onTap: onTap,
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppColors.primaryContainer.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: AppColors.primary, size: 20),
        ),
        title: Text(
          title,
          style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700),
        ),
        subtitle: Text(
          subtitle,
          style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant),
        ),
        trailing: const Icon(Icons.chevron_right, size: 20),
      ),
    );
  }
}
