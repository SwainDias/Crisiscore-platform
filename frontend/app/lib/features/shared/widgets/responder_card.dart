import 'package:flutter/material.dart';
import '../../../core/theme/colors.dart';
import '../../shared/models/incident_model.dart';

class ResponderCard extends StatelessWidget {
  final ResponderModel responder;

  const ResponderCard({super.key, required this.responder});

  @override
  Widget build(BuildContext context) {
    final isOnScene = responder.status == 'On Scene';
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: isOnScene ? AppColors.primaryContainer : AppColors.surfaceVariant,
              shape: BoxShape.circle,
            ),
            child: Center(
              child: Text(
                responder.id,
                style: Theme.of(context).textTheme.labelLarge?.copyWith(
                      color: isOnScene ? AppColors.onPrimaryContainer : AppColors.onSurfaceVariant,
                      fontWeight: FontWeight.w700,
                    ),
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  responder.name,
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600),
                ),
                Text(
                  'ETA: ${responder.eta} • ${responder.status}',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant),
                ),
              ],
            ),
          ),
          Icon(Icons.chevron_right, color: AppColors.outline),
        ],
      ),
    );
  }
}
