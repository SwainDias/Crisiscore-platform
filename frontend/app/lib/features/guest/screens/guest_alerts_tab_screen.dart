import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:latlong2/latlong.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';

class GuestAlertsTabScreen extends ConsumerStatefulWidget {
  const GuestAlertsTabScreen({super.key});

  @override
  ConsumerState<GuestAlertsTabScreen> createState() =>
      _GuestAlertsTabScreenState();
}

class _GuestAlertsTabScreenState extends ConsumerState<GuestAlertsTabScreen> {
  late Timer _timer;
  int _seconds = 4 * 60 + 23; // 00:04:23

  final List<bool> _checklistDone = [true, true, false, false];

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() => _seconds++);
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  String get _timeElapsed {
    final h = _seconds ~/ 3600;
    final m = (_seconds % 3600) ~/ 60;
    final s = _seconds % 60;
    return '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final hasActiveIncident = ref.watch(activeIncidentProvider);

    if (!hasActiveIncident) {
      return Scaffold(
        backgroundColor: AppColors.surface,
        body: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.surfaceContainerLow,
                  ),
                  child: const Icon(Icons.notifications_none, size: 40, color: AppColors.onSurfaceVariant),
                ),
                const SizedBox(height: 16),
                Text(
                  'No Active Alerts',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 8),
                Text(
                  'You\'re all clear. We\'ll notify you\nif anything changes.',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.surface,
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 12),
          child: Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () {},
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    side: BorderSide(color: AppColors.outlineVariant),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  ),
                  child: Text(
                    'Log Update',
                    style: TextStyle(color: AppColors.onSurface, fontWeight: FontWeight.w600),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                flex: 2,
                child: FilledButton(
                  onPressed: () {},
                  style: FilledButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  ),
                  child: const Text('Resolve Incident', style: TextStyle(fontWeight: FontWeight.w700)),
                ),
              ),
            ],
          ),
        ),
      ),
      body: CustomScrollView(
        slivers: [
          // App Bar
          SliverAppBar(
            pinned: true,
            backgroundColor: AppColors.surface.withValues(alpha: 0.95),
            automaticallyImplyLeading: false,
            title: Text('Emergency Response',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
            leading: IconButton(icon: const Icon(Icons.menu), onPressed: () {}),
            actions: [
              Padding(
                padding: const EdgeInsets.all(8),
                child: CircleAvatar(
                  radius: 16,
                  backgroundColor: AppColors.surfaceContainerHigh,
                  child: const Icon(Icons.person, size: 18, color: AppColors.onSurfaceVariant),
                ),
              ),
            ],
          ),

          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                const SizedBox(height: 8),

                // Active Incident Badge
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppColors.errorContainer,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.warning_amber_rounded, color: AppColors.onErrorContainer, size: 14),
                      const SizedBox(width: 6),
                      Text(
                        'Active Incident M-09',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: AppColors.onErrorContainer,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.3,
                            ),
                      ),
                    ],
                  ),
                ).animate().fadeIn(),

                const SizedBox(height: 16),

                // Incident Title
                Text(
                  'Medical\nEmergency',
                  style: Theme.of(context).textTheme.displaySmall?.copyWith(
                        fontWeight: FontWeight.w900,
                        color: AppColors.onSurface,
                        height: 1.05,
                      ),
                ).animate().fadeIn(delay: 50.ms),

                const SizedBox(height: 12),

                Text(
                  'Sector 4, Main Concourse. Subject unresponsive. EMS dispatched.',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.onSurfaceVariant,
                        height: 1.5,
                      ),
                ).animate().fadeIn(delay: 100.ms),

                const SizedBox(height: 24),

                // Timer
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceContainerLow,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'TIME ELAPSED',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: AppColors.onSurfaceVariant,
                              fontWeight: FontWeight.w700,
                              letterSpacing: 1.5,
                            ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        _timeElapsed,
                        style: Theme.of(context).textTheme.displayMedium?.copyWith(
                              color: AppColors.primary,
                              fontWeight: FontWeight.w700,
                              fontFeatures: const [FontFeature.tabularFigures()],
                              letterSpacing: -1,
                            ),
                      ),
                    ],
                  ),
                ).animate().fadeIn(delay: 150.ms),

                const SizedBox(height: 16),

                // OpenStreetMap
                Container(
                  height: 180,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    color: AppColors.surfaceContainerHigh,
                  ),
                  clipBehavior: Clip.antiAlias,
                  child: Stack(
                    children: [
                      FlutterMap(
                        options: const MapOptions(
                          initialCenter: LatLng(40.7128, -74.0060),
                          initialZoom: 16.5,
                          interactionOptions: InteractionOptions(
                            flags: InteractiveFlag.pinchZoom | InteractiveFlag.drag,
                          ),
                        ),
                        children: [
                          TileLayer(
                            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                            userAgentPackageName: 'com.resq.app',
                          ),
                          const MarkerLayer(
                            markers: [
                              Marker(
                                point: LatLng(40.7130, -74.0055),
                                width: 44,
                                height: 44,
                                child: Icon(Icons.location_pin, color: AppColors.primary, size: 44),
                              ),
                              Marker(
                                point: LatLng(40.7124, -74.0068),
                                width: 36,
                                height: 36,
                                child: Icon(Icons.local_hospital, color: AppColors.error, size: 36),
                              ),
                            ],
                          ),
                        ],
                      ),
                      // Map controls overlay
                      Positioned(
                        top: 10,
                        left: 10,
                        child: Column(
                          children: [
                            _MapButton(icon: Icons.layers),
                            const SizedBox(height: 6),
                            _MapButton(icon: Icons.my_location),
                          ],
                        ),
                      ),
                    ],
                  ),
                ).animate().fadeIn(delay: 200.ms),

                const SizedBox(height: 28),

                // Active Responders
                Text(
                  'Active Responders',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 12),

                _ResponderCard(
                  tag: 'R1',
                  tagColor: AppColors.primary,
                  name: 'Unit 4 - Alpha',
                  meta: 'ETA: 2 mins  •  En route',
                ).animate().fadeIn(delay: 250.ms),
                const SizedBox(height: 10),
                _ResponderCard(
                  tag: 'R2',
                  tagColor: AppColors.secondary,
                  name: 'EMS Ground',
                  meta: 'ETA: 5 mins  •  Dispatched',
                ).animate().fadeIn(delay: 290.ms),
                const SizedBox(height: 10),
                _ResponderCard(
                  tag: 'R3',
                  tagColor: AppColors.tertiary,
                  name: 'Security Team B',
                  meta: 'On Scene',
                ).animate().fadeIn(delay: 330.ms),

                const SizedBox(height: 16),

                // Request Backup Button
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () {},
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      side: const BorderSide(color: AppColors.primary),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                    ),
                    child: const Text(
                      'Request Backup',
                      style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.w700),
                    ),
                  ),
                ),

                const SizedBox(height: 28),

                // Standard Operating Procedure
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Standard Operating\nProcedure',
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                  fontWeight: FontWeight.w800,
                                  height: 1.2,
                                ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Medical Emergency Protocol',
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: AppColors.primaryContainer.withValues(alpha: 0.4),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        children: [
                          Text(
                            '2/5',
                            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                  fontWeight: FontWeight.w800,
                                  color: AppColors.primary,
                                ),
                          ),
                          Text(
                            'Completed',
                            style: Theme.of(context).textTheme.labelSmall?.copyWith(color: AppColors.onSurfaceVariant),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                _ChecklistItem(
                  title: 'Secure immediate area',
                  subtitle: 'Completed at 14:02',
                  done: _checklistDone[0],
                  onTap: () => setState(() => _checklistDone[0] = !_checklistDone[0]),
                ).animate().fadeIn(delay: 350.ms),
                const SizedBox(height: 8),
                _ChecklistItem(
                  title: 'Dispatch EMS',
                  subtitle: 'Completed at 14:03',
                  done: _checklistDone[1],
                  onTap: () => setState(() => _checklistDone[1] = !_checklistDone[1]),
                ).animate().fadeIn(delay: 380.ms),
                const SizedBox(height: 8),
                _ChecklistItem(
                  title: 'Clear path for EMS',
                  subtitle: 'Ensure elevators and main corridors are held open for arriving teams.',
                  done: _checklistDone[2],
                  onTap: () => setState(() => _checklistDone[2] = !_checklistDone[2]),
                ).animate().fadeIn(delay: 410.ms),
                const SizedBox(height: 8),
                _ChecklistItem(
                  title: 'Notify family/emergency contact',
                  subtitle: 'Pending identity confirmation',
                  done: _checklistDone[3],
                  onTap: () => setState(() => _checklistDone[3] = !_checklistDone[3]),
                ).animate().fadeIn(delay: 440.ms),

                const SizedBox(height: 100),
              ]),
            ),
          ),
        ],
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
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.1), blurRadius: 8)],
      ),
      child: Icon(icon, size: 18, color: AppColors.onSurface),
    );
  }
}

class _ResponderCard extends StatelessWidget {
  final String tag;
  final Color tagColor;
  final String name;
  final String meta;

  const _ResponderCard({
    required this.tag,
    required this.tagColor,
    required this.name,
    required this.meta,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: tagColor.withValues(alpha: 0.15),
            ),
            child: Center(
              child: Text(
                tag,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: tagColor,
                      fontWeight: FontWeight.w800,
                    ),
              ),
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 2),
                Text(meta, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
              ],
            ),
          ),
          const Icon(Icons.chevron_right, color: AppColors.onSurfaceVariant, size: 20),
        ],
      ),
    );
  }
}

class _ChecklistItem extends StatelessWidget {
  final String title;
  final String subtitle;
  final bool done;
  final VoidCallback onTap;

  const _ChecklistItem({
    required this.title,
    required this.subtitle,
    required this.done,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surfaceContainerLowest,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: done ? AppColors.primary.withValues(alpha: 0.3) : AppColors.outlineVariant.withValues(alpha: 0.3),
          ),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 24,
              height: 24,
              margin: const EdgeInsets.only(top: 1),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: done ? AppColors.primary : Colors.transparent,
                border: done ? null : Border.all(color: AppColors.outlineVariant),
              ),
              child: done
                  ? const Icon(Icons.check, color: Colors.white, size: 14)
                  : null,
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: Theme.of(context).textTheme.titleSmall?.copyWith(
                          fontWeight: FontWeight.w700,
                          color: done ? AppColors.onSurfaceVariant : AppColors.onSurface,
                          decoration: done ? TextDecoration.lineThrough : null,
                        ),
                  ),
                  if (subtitle.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: AppColors.onSurfaceVariant,
                            height: 1.4,
                          ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
