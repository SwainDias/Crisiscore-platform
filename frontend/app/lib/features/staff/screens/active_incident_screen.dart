import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/responder_card.dart';
import '../../shared/widgets/sop_step_card.dart';
import '../../shared/widgets/pulse_indicator.dart';
import '../../shared/widgets/resq_map_widget.dart';

class ActiveIncidentScreen extends ConsumerStatefulWidget {
  final String incidentId;
  const ActiveIncidentScreen({super.key, required this.incidentId});

  @override
  ConsumerState<ActiveIncidentScreen> createState() => _ActiveIncidentScreenState();
}

class _ActiveIncidentScreenState extends ConsumerState<ActiveIncidentScreen> {
  late Timer _timer;
  Duration _elapsed = const Duration(minutes: 4, seconds: 23);

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() => _elapsed += const Duration(seconds: 1));
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  String get _elapsedStr {
    final h = _elapsed.inHours.toString().padLeft(2, '0');
    final m = (_elapsed.inMinutes % 60).toString().padLeft(2, '0');
    final s = (_elapsed.inSeconds % 60).toString().padLeft(2, '0');
    return '$h:$m:$s';
  }

  @override
  Widget build(BuildContext context) {
    final incident = mockIncident;
    final completedSteps = incident.sopSteps.where((s) => s.done).length;

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.pop()),
        title: Text('Emergency Response', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status badge & title
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppColors.errorContainer,
                    borderRadius: BorderRadius.circular(9999),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.warning, size: 14, color: AppColors.onErrorContainer),
                      const SizedBox(width: 6),
                      Text('Active Incident M-09',
                          style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                color: AppColors.onErrorContainer,
                                fontWeight: FontWeight.w600,
                              )),
                    ],
                  ),
                ),
                const Spacer(),
                const PulseIndicator(color: AppColors.error, size: 8),
              ],
            ).animate().fadeIn(),

            const SizedBox(height: 16),

            Text('Medical Emergency',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            Text(incident.detail,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant)),

            const SizedBox(height: 20),

            // Time elapsed
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.surfaceContainerLow,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  Text('TIME ELAPSED',
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: AppColors.onSurfaceVariant,
                            letterSpacing: 1.5,
                          )),
                  const SizedBox(height: 8),
                  Text(_elapsedStr,
                      style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                            color: AppColors.error,
                            fontWeight: FontWeight.w700,
                          )),
                ],
              ),
            ).animate().fadeIn(delay: 100.ms),

            const SizedBox(height: 20),

            SizedBox(
              height: 200,
              child: Stack(
                children: [
                  const Positioned.fill(
                    child: ResQMapWidget(
                      interactive: false,
                      showIncidentPin: true,
                      showStaffDots: true,
                      showEvacRoute: true,
                    ),
                  ),
                  Positioned(
                    top: 12,
                    left: 12,
                    child: Row(
                      children: [
                        _MapButton(icon: Icons.layers),
                        const SizedBox(width: 8),
                        _MapButton(icon: Icons.my_location),
                      ],
                    ),
                  ),
                ],
              ),
            ).animate().fadeIn(delay: 200.ms),

            const SizedBox(height: 20),

            // Responders
            Text('Active Responders',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 12),
            ...incident.responders.map((r) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: ResponderCard(responder: r),
                )),

            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () {},
                style: FilledButton.styleFrom(backgroundColor: AppColors.secondaryContainer),
                child: Text('Request Backup', style: TextStyle(color: AppColors.onSecondaryContainer)),
              ),
            ),

            const SizedBox(height: 24),

            // SOP
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Standard Operating Procedure',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
                    Text('Medical Emergency Protocol',
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.primaryFixed,
                    borderRadius: BorderRadius.circular(9999),
                  ),
                  child: Text('$completedSteps/${incident.sopSteps.length} Completed',
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: AppColors.primary,
                            fontWeight: FontWeight.w600,
                          )),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ...incident.sopSteps.map((s) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: SopStepCard(step: s),
                )),

            const SizedBox(height: 24),

            // Action buttons
            Row(
              children: [
                Expanded(
                  child: FilledButton(
                    onPressed: () {
                      showModalBottomSheet(
                        context: context,
                        builder: (ctx) => _LogUpdateSheet(),
                      );
                    },
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.surfaceContainerHighest,
                      foregroundColor: AppColors.onSurface,
                    ),
                    child: const Text('Log Update'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(9999),
                      gradient: const LinearGradient(
                        colors: [AppColors.primary, AppColors.primaryContainer],
                      ),
                    ),
                    child: FilledButton(
                      onPressed: () {
                        ref.read(activeIncidentProvider.notifier).setActive(false);
                        context.push('/staff/post-incident/${widget.incidentId}');
                      },
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.transparent,
                        shadowColor: Colors.transparent,
                      ),
                      child: const Text('Resolve Incident'),
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}

class _MapButton extends StatelessWidget {
  final IconData icon;
  const _MapButton({required this.icon});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: AppColors.surfaceContainerLowest.withValues(alpha: 0.7),
      ),
      child: Icon(icon, size: 20, color: AppColors.onSurface),
    );
  }
}

class _LogUpdateSheet extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: const BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.outlineVariant,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          const SizedBox(height: 20),
          Text('Log Update', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 16),
          const TextField(
            maxLines: 4,
            decoration: InputDecoration(hintText: 'Describe what happened...'),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: FilledButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Submit Update'),
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
