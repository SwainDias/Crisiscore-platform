import 'package:flutter/material.dart';

import '../../../core/theme/colors.dart';
import '../../shared/widgets/resq_map_widget.dart';

class StaffMapTabScreen extends StatelessWidget {
  const StaffMapTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Operational Map',
                style: Theme.of(context)
                    .textTheme
                    .headlineSmall
                    ?.copyWith(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 8),
              Text(
                'Live responder positions and evacuation guidance.',
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(color: AppColors.onSurfaceVariant),
              ),
              const SizedBox(height: 16),
              const Expanded(
                child: ResQMapWidget(
                  interactive: true,
                  showIncidentPin: true,
                  showStaffDots: true,
                  showEvacRoute: true,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
