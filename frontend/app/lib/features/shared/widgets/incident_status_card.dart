import 'package:flutter/material.dart';
import '../../../core/theme/colors.dart';
import '../../shared/models/incident_model.dart';
import 'pulse_indicator.dart';

class IncidentStatusCard extends StatelessWidget {
  final IncidentModel incident;
  final VoidCallback? onViewDetails;

  const IncidentStatusCard({
    super.key,
    required this.incident,
    this.onViewDetails,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.errorContainer,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppColors.error.withValues(alpha: 0.1),
            blurRadius: 30,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: const BoxDecoration(
                  color: AppColors.error,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.warning_rounded, color: Colors.white, size: 24),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            'Active Incident: ${incident.location}',
                            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                  color: AppColors.onErrorContainer,
                                  fontWeight: FontWeight.w700,
                                ),
                          ),
                        ),
                        const PulseIndicator(color: AppColors.error, size: 8),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      incident.detail,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: AppColors.onErrorContainer.withValues(alpha: 0.9),
                          ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: FilledButton(
              onPressed: onViewDetails,
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.error,
                foregroundColor: Colors.white,
              ),
              child: const Text('View Details'),
            ),
          ),
        ],
      ),
    );
  }
}
