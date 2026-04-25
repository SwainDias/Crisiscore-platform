import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';

class GuestAlertsTabScreen extends ConsumerWidget {
  const GuestAlertsTabScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final hasActiveIncident = ref.watch(activeIncidentProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Alerts',
                style: Theme.of(context)
                    .textTheme
                    .headlineSmall
                    ?.copyWith(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 12),
              if (hasActiveIncident)
                Card(
                  color: AppColors.errorContainer,
                  child: ListTile(
                    leading: const Icon(Icons.warning_amber_rounded),
                    title: const Text('Active hotel alert'),
                    subtitle: const Text('Tap to view safety instructions.'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => context.push('/guest/instructions'),
                  ),
                )
              else
                Expanded(
                  child: Center(
                    child: Text(
                      'No active alerts',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
