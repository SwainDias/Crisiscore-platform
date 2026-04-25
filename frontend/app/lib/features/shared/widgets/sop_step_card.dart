import 'package:flutter/material.dart';
import '../../../core/theme/colors.dart';
import '../../shared/models/incident_model.dart';

class SopStepCard extends StatelessWidget {
  final SOPStep step;

  const SopStepCard({super.key, required this.step});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: step.isActive ? AppColors.surfaceContainerLowest : AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: step.isActive
            ? Border.all(color: AppColors.outlineVariant.withValues(alpha: 0.15))
            : null,
        boxShadow: step.isActive
            ? [BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.06), blurRadius: 40)]
            : null,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 2),
            child: Icon(
              step.done ? Icons.check_circle : Icons.radio_button_unchecked,
              color: step.done ? AppColors.primary : AppColors.outline,
              size: 24,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  step.text,
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                        fontWeight: FontWeight.w600,
                        decoration: step.done ? TextDecoration.lineThrough : null,
                        fontSize: step.isActive ? 16 : 14,
                      ),
                ),
                if (step.completedAt != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    'Completed at ${step.completedAt}',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: AppColors.onSurfaceVariant,
                        ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
