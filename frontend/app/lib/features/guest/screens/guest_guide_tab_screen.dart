import 'package:flutter/material.dart';

import '../../../core/theme/colors.dart';

class GuestGuideTabScreen extends StatelessWidget {
  const GuestGuideTabScreen({super.key});

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
              'Emergency procedures and preparedness steps.',
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium
                  ?.copyWith(color: AppColors.onSurfaceVariant),
            ),
            const SizedBox(height: 20),
            Card(
              child: ListTile(
                leading: const Icon(Icons.shield_outlined),
                title: const Text('Shelter-in-Place Basics'),
                subtitle: const Text('How to stay safe during indoor alerts.'),
              ),
            ),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                leading: const Icon(Icons.route_outlined),
                title: const Text('Evacuation Readiness'),
                subtitle: const Text('Know your nearest exit and assembly point.'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
