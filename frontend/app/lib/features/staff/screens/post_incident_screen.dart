import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';

class PostIncidentScreen extends StatelessWidget {
  final String incidentId;
  const PostIncidentScreen({super.key, required this.incidentId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.go('/staff/home')),
        title: Row(
          children: [
            const Icon(Icons.emergency, color: AppColors.primary),
            const SizedBox(width: 8),
            Text('ResQ', style: Theme.of(context).textTheme.titleLarge?.copyWith(color: AppColors.primary, fontWeight: FontWeight.w800)),
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.download), onPressed: () {}),
          IconButton(icon: const Icon(Icons.share), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status badge
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(color: AppColors.secondaryFixed, borderRadius: BorderRadius.circular(9999)),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.check_circle, size: 14, color: AppColors.onSecondaryContainer),
                  const SizedBox(width: 6),
                  Text('INCIDENT RESOLVED',
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: AppColors.onSecondaryContainer,
                            fontWeight: FontWeight.w700,
                          )),
                ],
              ),
            ).animate().fadeIn(),

            const SizedBox(height: 16),

            Text('Post-Incident Summary:\nSector 4 Evacuation',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800, height: 1.2)),
            const SizedBox(height: 8),
            Text('Event ID: #RQ-2023-11A • Concluded Oct 24, 14:30 EST',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant)),

            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.description),
              label: const Text('Export Full Report'),
            ),

            const SizedBox(height: 24),

            // Metrics
            Row(
              children: [
                Expanded(child: _MetricCard(icon: Icons.timer, title: 'Response Time', value: '4m 12s', sub: '-1m 48s vs SLA')),
                const SizedBox(width: 12),
                Expanded(child: _MetricCard(icon: Icons.group, title: 'Personnel', value: '142/142', sub: '100% Verified')),
              ],
            ).animate().fadeIn(delay: 100.ms),
            const SizedBox(height: 12),
            _MetricCard(icon: Icons.fact_check, title: 'SOP Compliance', value: '98%', sub: '1 minor deviation').animate().fadeIn(delay: 200.ms),

            const SizedBox(height: 24),

            // Timeline
            Text('Event Timeline', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 16),

            _TimelineItem(time: '12:45 PM', title: 'Initial Alert Triggered',
                desc: 'Smoke detected in Sector 4. Automated alarm sounded.',
                icon: Icons.warning, isFirst: true),
            _TimelineItem(time: '12:48 PM', title: 'Evacuation Commenced',
                desc: 'Area Wardens initiated sweep. Main exits cleared.', icon: Icons.directions_run),
            _TimelineItem(time: '12:55 PM', title: 'Emergency Services Arrived',
                desc: 'Fire department on scene. Handoff completed.', icon: Icons.local_fire_department),
            _TimelineItem(time: '14:30 PM', title: 'All Clear & Debrief',
                desc: 'Incident stood down. Personnel accounted for.', icon: Icons.verified, isLast: true),

            const SizedBox(height: 24),

            // Improvement opportunities
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppColors.secondaryFixed.withValues(alpha: 0.5),
                borderRadius: BorderRadius.circular(24),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.trending_up, color: AppColors.secondary),
                      const SizedBox(width: 12),
                      Text('Improvement Opportunities',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                color: AppColors.secondary,
                                fontWeight: FontWeight.w700,
                              )),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'While the response exceeded SLA targets, post-incident analysis identified minor areas for refinement.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant, height: 1.5),
                  ),
                  const SizedBox(height: 16),
                  _ImprovementItem(title: 'Comms Relay Delay',
                      desc: '45s delay noted in secondary channel. Recommend network priority review.'),
                  const SizedBox(height: 12),
                  _ImprovementItem(title: 'Exit Point Congestion',
                      desc: 'Minor bottleneck at East stairwell. Consider alternate routing.'),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.edit_note),
                      label: const Text('Log Action Item'),
                      style: FilledButton.styleFrom(
                        backgroundColor: AppColors.surfaceContainerHighest,
                        foregroundColor: AppColors.onSurface,
                      ),
                    ),
                  ),
                ],
              ),
            ).animate().fadeIn(delay: 300.ms),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;
  final String sub;
  const _MetricCard({required this.icon, required this.title, required this.value, required this.sub});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: AppColors.primary, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(title,
                    style: Theme.of(context).textTheme.labelLarge?.copyWith(color: AppColors.onSurfaceVariant)),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(value, style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 4),
          Text(sub, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.outline)),
        ],
      ),
    );
  }
}

class _TimelineItem extends StatelessWidget {
  final String time;
  final String title;
  final String desc;
  final IconData icon;
  final bool isFirst;
  final bool isLast;
  const _TimelineItem({required this.time, required this.title, required this.desc, required this.icon, this.isFirst = false, this.isLast = false});

  @override
  Widget build(BuildContext context) {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 40,
            child: Column(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isFirst ? AppColors.primaryContainer : AppColors.surfaceVariant,
                  ),
                  child: Icon(icon, size: 16, color: isFirst ? AppColors.onPrimary : AppColors.onSurfaceVariant),
                ),
                if (!isLast) Expanded(child: Container(width: 2, color: AppColors.surfaceVariant)),
              ],
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isFirst ? AppColors.surfaceContainerLow : AppColors.surface,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(time,
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: isFirst ? AppColors.primary : AppColors.onSurfaceVariant,
                              fontWeight: FontWeight.w700,
                            )),
                    const SizedBox(height: 4),
                    Text(title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                    const SizedBox(height: 4),
                    Text(desc, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ImprovementItem extends StatelessWidget {
  final String title;
  final String desc;
  const _ImprovementItem({required this.title, required this.desc});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(Icons.arrow_right, color: AppColors.tertiaryContainer, size: 20),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: Theme.of(context).textTheme.labelLarge?.copyWith(fontWeight: FontWeight.w600)),
              const SizedBox(height: 2),
              Text(desc, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
            ],
          ),
        ),
      ],
    );
  }
}
