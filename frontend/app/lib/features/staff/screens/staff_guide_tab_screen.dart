import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';

class StaffGuideTabScreen extends StatelessWidget {
  const StaffGuideTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Guide',
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            Text(
              'Training and quiet safety tools.',
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(color: AppColors.onSurfaceVariant),
            ),
            const SizedBox(height: 20),
            Card(
              child: ListTile(
                leading: const Icon(Icons.school_outlined),
                title: const Text('Training Drill'),
                subtitle: const Text('Run a short response simulation.'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => context.push('/staff/drill/1'),
              ),
            ),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                leading: const Icon(Icons.health_and_safety_outlined),
                title: const Text('Staff Safety Check'),
                subtitle: const Text('Open the discreet safety-check screen.'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => context.push('/staff/silent-panic'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
