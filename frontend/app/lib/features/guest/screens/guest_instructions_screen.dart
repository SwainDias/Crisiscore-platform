import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/resq_map_widget.dart';

class GuestInstructionsScreen extends StatelessWidget {
  const GuestInstructionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.surfaceContainerLowest.withValues(alpha: 0.7),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
        title: Row(
          children: [
            const Icon(Icons.emergency, color: AppColors.primary),
            const SizedBox(width: 8),
            Text('ResQ',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.primary,
                      fontWeight: FontWeight.w800,
                    )),
          ],
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.all(8),
            child: CircleAvatar(
              radius: 18,
              backgroundColor: AppColors.surfaceContainerHigh,
              child: const Icon(Icons.person, size: 20, color: AppColors.onSurfaceVariant),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Emergency Banner
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.errorContainer,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.warning, color: AppColors.error, size: 28),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Active Alert: Shelter in Place',
                            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                  color: AppColors.onErrorContainer,
                                  fontWeight: FontWeight.w700,
                                )),
                        const SizedBox(height: 8),
                        Text(
                          'A severe weather event has been detected in the area. Please follow the instructions below and remain indoors until the all-clear is given.',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: AppColors.onErrorContainer.withValues(alpha: 0.9),
                                height: 1.5,
                              ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ).animate().fadeIn(),

            const SizedBox(height: 24),

            // Primary instruction card
            Container(
              padding: const EdgeInsets.all(28),
              decoration: BoxDecoration(
                color: AppColors.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.06), blurRadius: 40),
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: AppColors.secondaryFixed,
                            borderRadius: BorderRadius.circular(9999),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.door_front_door, size: 14, color: AppColors.onSecondaryContainer),
                              const SizedBox(width: 6),
                              Text('Room ${mockGuest.room}',
                                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                        color: AppColors.onSecondaryContainer,
                                        fontWeight: FontWeight.w700,
                                      )),
                            ],
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text('Stay in your room',
                            style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
                        const SizedBox(height: 12),
                        Text(
                          'Lock all doors and windows. Draw the curtains and stay away from glass. Your room is structurally sound and designated as a safe zone.',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: AppColors.onSurfaceVariant,
                                height: 1.5,
                              ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 16),
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppColors.primaryContainer.withValues(alpha: 0.1),
                    ),
                    child: const Icon(Icons.meeting_room, color: AppColors.primary, size: 40),
                  ),
                ],
              ),
            ).animate().fadeIn(delay: 100.ms),

            const SizedBox(height: 28),

            // Step-by-step instructions
            Text('Immediate Actions',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 16),

            _StepCard(step: 1, title: 'Secure the Perimeter',
                desc: 'Ensure your main door is locked and the deadbolt is engaged. Close and latch all windows.')
                .animate().fadeIn(delay: 200.ms).slideX(begin: -0.05),
            const SizedBox(height: 12),
            _StepCard(step: 2, title: 'Minimize Hazards',
                desc: 'Draw all curtains and blinds to protect against potential glass breakage. Move away from exterior walls.')
                .animate().fadeIn(delay: 300.ms).slideX(begin: -0.05),
            const SizedBox(height: 12),
            _StepCard(step: 3, title: 'Stay Informed',
                desc: 'Keep your mobile device charged and monitor this app for further updates from hotel security.')
                .animate().fadeIn(delay: 400.ms).slideX(begin: -0.05),

            const SizedBox(height: 28),

            // Evacuation routes
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.surfaceContainerLow,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('Evacuation Routes',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
                      FilledButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.open_in_full, size: 16),
                        label: const Text('Expand'),
                        style: FilledButton.styleFrom(
                          backgroundColor: AppColors.secondaryContainer,
                          foregroundColor: AppColors.onSecondaryContainer,
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  SizedBox(
                    height: 160,
                    child: Stack(
                      children: [
                        const Positioned.fill(
                          child: ResQMapWidget(
                            interactive: false,
                            showIncidentPin: false,
                            showStaffDots: false,
                            showEvacRoute: true,
                          ),
                        ),
                        Center(
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(
                              color: AppColors.surface.withValues(alpha: 0.8),
                              borderRadius: BorderRadius.circular(9999),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.location_on, color: AppColors.error, size: 16),
                                const SizedBox(width: 6),
                                Text('You are here',
                                    style: Theme.of(context).textTheme.labelMedium?.copyWith(fontWeight: FontWeight.w500)),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ).animate().fadeIn(delay: 500.ms),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}

class _StepCard extends StatelessWidget {
  final int step;
  final String title;
  final String desc;

  const _StepCard({required this.step, required this.title, required this.desc});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.primary,
              boxShadow: [BoxShadow(color: AppColors.primary.withValues(alpha: 0.2), blurRadius: 8)],
            ),
            child: Center(
              child: Text('$step',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      )),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                const SizedBox(height: 4),
                Text(desc,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppColors.onSurfaceVariant,
                          height: 1.5,
                        )),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
