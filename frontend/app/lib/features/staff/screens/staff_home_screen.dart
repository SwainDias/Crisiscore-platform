import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/incident_status_card.dart';
import '../../shared/widgets/role_badge.dart';
import '../../shared/widgets/resq_map_widget.dart';

class StaffHomeScreen extends ConsumerWidget {
  const StaffHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final hasActive = ref.watch(activeIncidentProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          // App bar
          SliverAppBar(
            pinned: true,
            floating: true,
            backgroundColor: AppColors.surface.withValues(alpha: 0.8),
            automaticallyImplyLeading: false,
            title: Row(
              children: [
                Icon(Icons.emergency, color: AppColors.primary, size: 24),
                const SizedBox(width: 8),
                Text('ResQ',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.w800,
                        )),
              ],
            ),
            actions: [
              CircleAvatar(
                radius: 20,
                backgroundColor: AppColors.surfaceContainerHigh,
                child: const Icon(Icons.person, color: AppColors.onSurfaceVariant),
              ),
              const SizedBox(width: 16),
            ],
          ),

          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // Active incident banner
                if (hasActive) ...[
                  IncidentStatusCard(
                    incident: mockIncident,
                    onViewDetails: () => context.push('/staff/incident/${mockIncident.id}'),
                  ).animate().fadeIn().slideY(begin: -0.1),
                  const SizedBox(height: 24),
                ],

                // My Status Card
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceContainerLowest,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.onSurface.withValues(alpha: 0.03),
                        blurRadius: 40,
                        offset: const Offset(0, 20),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text('My Status',
                              style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                          const RoleBadge(label: 'On Duty'),
                        ],
                      ),
                      const SizedBox(height: 20),
                      Row(
                        children: [
                          Container(
                            width: 64,
                            height: 64,
                            decoration: const BoxDecoration(
                              shape: BoxShape.circle,
                              color: AppColors.primaryContainer,
                            ),
                            child: const Icon(Icons.shield, color: AppColors.onPrimaryContainer, size: 32),
                          ),
                          const SizedBox(width: 20),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Current Assignment',
                                  style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
                              const SizedBox(height: 4),
                              Text('Sector 4 Evac',
                                  style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),
                      _InfoRow(label: 'Check-in Time', value: mockStaff.shiftStart),
                      const Divider(height: 20, color: AppColors.surfaceVariant),
                      _InfoRow(label: 'Vehicle', value: 'Unit 42 (SUV)'),
                    ],
                  ),
                ).animate().fadeIn(delay: 100.ms),

                const SizedBox(height: 20),

                // Trigger Alert Button
                GestureDetector(
                  onTap: () => context.push('/staff/trigger'),
                  child: Container(
                    padding: const EdgeInsets.all(28),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      gradient: LinearGradient(
                        colors: [AppColors.error, const Color(0xFF93000A)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.error.withValues(alpha: 0.2),
                          blurRadius: 40,
                          offset: const Offset(0, 20),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: Colors.white.withValues(alpha: 0.2),
                          ),
                          child: const Icon(Icons.sos, color: Colors.white, size: 40),
                        ),
                        const SizedBox(height: 16),
                        Text('Trigger Alert',
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w700,
                                )),
                        const SizedBox(height: 8),
                        Text(
                          'Broadcast immediate emergency to all available units',
                          textAlign: TextAlign.center,
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.white.withValues(alpha: 0.8)),
                        ),
                      ],
                    ),
                  ),
                ).animate().fadeIn(delay: 200.ms),

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
                          showEvacRoute: false,
                        ),
                      ),
                      Positioned(
                        bottom: 16,
                        left: 16,
                        right: 16,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('Live Map',
                                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                          color: Colors.white,
                                          fontWeight: FontWeight.w700,
                                        )),
                                const SizedBox(height: 4),
                                Text('3 Active Zones • 12 Units',
                                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.white70)),
                              ],
                            ),
                            Container(
                              width: 44,
                              height: 44,
                              decoration: const BoxDecoration(
                                shape: BoxShape.circle,
                                color: AppColors.surfaceContainerLowest,
                              ),
                              child: const Icon(Icons.arrow_forward, color: AppColors.primary),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ).animate().fadeIn(delay: 300.ms),

                const SizedBox(height: 20),

                // Tasks & History row
                Row(
                  children: [
                    Expanded(child: _TasksCard()),
                    const SizedBox(width: 16),
                    Expanded(child: _HistoryCard()),
                  ],
                ).animate().fadeIn(delay: 400.ms),

                const SizedBox(height: 32),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;
  const _InfoRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
        Text(value, style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w500)),
      ],
    );
  }
}

class _TasksCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.checklist, color: AppColors.primaryContainer, size: 20),
              const SizedBox(width: 8),
              Text('My Tasks', style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
            ],
          ),
          const SizedBox(height: 16),
          _TaskItem(text: 'Deliver supplies to Point Alpha', priority: 'High Priority', isHigh: true),
          const SizedBox(height: 12),
          _TaskItem(text: 'Equipment check: Comm Radio', priority: 'Routine', isHigh: false),
          const SizedBox(height: 16),
          Text('View all tasks ›',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(color: AppColors.primary, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}

class _TaskItem extends StatelessWidget {
  final String text;
  final String priority;
  final bool isHigh;
  const _TaskItem({required this.text, required this.priority, required this.isHigh});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 20,
          height: 20,
          margin: const EdgeInsets.only(top: 2),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            border: Border.all(color: isHigh ? AppColors.primary : AppColors.outline, width: 2),
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(text, style: Theme.of(context).textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w500)),
              const SizedBox(height: 2),
              Text(priority,
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: isHigh ? AppColors.error : AppColors.onSurfaceVariant,
                      )),
            ],
          ),
        ),
      ],
    );
  }
}

class _HistoryCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.history, color: AppColors.tertiary, size: 20),
              const SizedBox(width: 8),
              Text('History', style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
            ],
          ),
          const SizedBox(height: 16),
          _HistoryItem(time: 'Today, 08:30 AM', text: 'Completed Evac Route B'),
          const SizedBox(height: 12),
          _HistoryItem(time: 'Yesterday, 14:00', text: 'Resolved Medical Alert #402'),
          const SizedBox(height: 16),
          Text('Full log ›',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(color: AppColors.tertiary, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}

class _HistoryItem extends StatelessWidget {
  final String time;
  final String text;
  const _HistoryItem({required this.time, required this.text});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            Container(width: 10, height: 10, decoration: BoxDecoration(shape: BoxShape.circle, color: AppColors.surfaceVariant)),
            Container(width: 2, height: 20, color: AppColors.surfaceVariant),
          ],
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(time, style: Theme.of(context).textTheme.labelSmall?.copyWith(color: AppColors.onSurfaceVariant)),
              const SizedBox(height: 2),
              Text(text, style: Theme.of(context).textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w500)),
            ],
          ),
        ),
      ],
    );
  }
}
