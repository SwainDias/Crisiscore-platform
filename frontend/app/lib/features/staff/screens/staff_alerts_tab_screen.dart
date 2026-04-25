import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/incident_status_card.dart';

class StaffAlertsTabScreen extends ConsumerWidget {
  const StaffAlertsTabScreen({super.key});

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
              const SizedBox(height: 8),
              Text(
                hasActiveIncident
                    ? 'A critical incident is active.'
                    : 'No active incidents right now.',
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(color: AppColors.onSurfaceVariant),
              ),
              const SizedBox(height: 16),
              if (hasActiveIncident)
                IncidentStatusCard(
                  incident: mockIncident,
                  onViewDetails: () =>
                      context.push('/staff/incident/${mockIncident.id}'),
                )
              else
                Expanded(
                  child: Center(
                    child: Text(
                      'All clear',
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
