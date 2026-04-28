import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/pulse_indicator.dart';

class GuestHomeScreen extends ConsumerWidget {
  const GuestHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final hasActive = ref.watch(activeIncidentProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      floatingActionButton: Padding(
        padding: const EdgeInsets.only(bottom: 16.0),
        child: FloatingActionButton(
          onPressed: () => context.push('/guest/trigger'),
          backgroundColor: AppColors.primary,
          shape: const CircleBorder(),
          elevation: 4,
          child: const Text('SOS', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900)),
        ),
      ),
      body: CustomScrollView(
        slivers: [
          // App bar
          SliverAppBar(
            pinned: true,
            floating: true,
            backgroundColor: AppColors.surface.withValues(alpha: 0.9),
            automaticallyImplyLeading: false,
            title: Text('Emergency Response',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
            leading: IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {},
            ),
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
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // Welcome hero
                RichText(
                  text: TextSpan(
                    style: Theme.of(context).textTheme.displaySmall?.copyWith(fontWeight: FontWeight.w700, color: AppColors.onSurface, height: 1.1),
                    children: [
                      const TextSpan(text: 'Stay Safe,\n'),
                      TextSpan(
                        text: '${mockGuest.name}.',
                        style: const TextStyle(color: AppColors.primary),
                      ),
                    ],
                  ),
                ).animate().fadeIn(duration: 500.ms),

                const SizedBox(height: 16),
                RichText(
                  text: TextSpan(
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant, height: 1.5),
                    children: [
                      const TextSpan(text: 'You are currently checked into '),
                      TextSpan(text: mockGuest.hotel, style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.onSurface)),
                      const TextSpan(text: '. Your safety is our priority.'),
                    ],
                  ),
                ).animate().fadeIn(delay: 100.ms),

                const SizedBox(height: 24),

                // Active alert card
                if (hasActive)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: AppColors.errorContainer.withValues(alpha: 0.7),
                      borderRadius: BorderRadius.circular(32),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 48,
                          height: 48,
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            color: AppColors.onErrorContainer,
                          ),
                          child: const Icon(Icons.campaign, color: Colors.white, size: 24),
                        ),
                        const SizedBox(height: 20),
                        Row(
                          children: [
                            Text('ACTIVE ALERT',
                                style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                      color: AppColors.onErrorContainer,
                                      fontWeight: FontWeight.w800,
                                      letterSpacing: 1.2,
                                    )),
                            const SizedBox(width: 8),
                            const PulseIndicator(color: AppColors.error, size: 6),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text('Severe Weather\nWarning',
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  color: AppColors.onErrorContainer,
                                  fontWeight: FontWeight.w700,
                                  height: 1.2,
                                )),
                        const SizedBox(height: 12),
                        Text(
                          'A severe thunderstorm warning has been issued for your area. Please remain indoors and stay away from windows until the all-clear is given.',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: AppColors.onErrorContainer.withValues(alpha: 0.9),
                                height: 1.5,
                              ),
                        ),
                        const SizedBox(height: 24),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            onPressed: () => context.push('/guest/instructions'),
                            style: FilledButton.styleFrom(
                              backgroundColor: AppColors.onErrorContainer,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                            ),
                            child: const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text('View Details', style: TextStyle(fontWeight: FontWeight.w600)),
                                SizedBox(width: 8),
                                Icon(Icons.arrow_forward, size: 18),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.1),

                const SizedBox(height: 32),

                // Quick Actions
                Text('Quick Actions',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 16),

                Column(
                  children: [
                    _ActionCard(
                      icon: Icons.phone_in_talk,
                      iconColor: AppColors.primary,
                      iconBg: AppColors.primaryContainer.withValues(alpha: 0.3),
                      title: 'Call for Help',
                      subtitle: 'Instantly connect with emergency services or hotel security.',
                    ).animate().fadeIn(delay: 300.ms),
                    const SizedBox(height: 12),
                    _ActionCard(
                      icon: Icons.meeting_room,
                      iconColor: AppColors.primary,
                      iconBg: AppColors.primaryContainer.withValues(alpha: 0.3),
                      title: 'Exit Routes',
                      subtitle: 'View the fastest and safest evacuation paths from your room.',
                    ).animate().fadeIn(delay: 350.ms),
                    const SizedBox(height: 12),
                    _ActionCard(
                      icon: Icons.verified_user,
                      iconColor: AppColors.onSurfaceVariant,
                      iconBg: AppColors.surfaceVariant,
                      title: 'Safe Zones',
                      subtitle: 'Locate designated assembly areas within the property.',
                    ).animate().fadeIn(delay: 400.ms),
                  ],
                ),

                const SizedBox(height: 32),

                // Information Hub
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Information Hub',
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                    TextButton(
                      onPressed: () {},
                      child: Row(
                        children: [
                          const Text('See All', style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.w600)),
                          const SizedBox(width: 4),
                          const Icon(Icons.arrow_forward, size: 16, color: AppColors.primary),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                _InfoHubCard(icon: Icons.local_fire_department, category: 'PROTOCOL', title: 'Fire Safety Procedures',
                    subtitle: 'Review what to do in case of...').animate().fadeIn(delay: 500.ms),
                const SizedBox(height: 12),
                _InfoHubCard(icon: Icons.medical_services, category: 'RESOURCES', title: 'First Aid Locations',
                    subtitle: 'Find nearby medical kits and...').animate().fadeIn(delay: 550.ms),

                const SizedBox(height: 100),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final Color? iconBg;
  final String title;
  final String subtitle;

  const _ActionCard({
    required this.icon,
    required this.iconColor,
    this.iconBg,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(32),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: iconBg ?? AppColors.primary.withValues(alpha: 0.1),
            ),
            child: Icon(icon, color: iconColor, size: 24),
          ),
          const SizedBox(height: 16),
          Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 8),
          Text(subtitle,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant, height: 1.4)),
        ],
      ),
    );
  }
}

class _InfoHubCard extends StatelessWidget {
  final IconData icon;
  final String category;
  final String title;
  final String subtitle;

  const _InfoHubCard({required this.icon, required this.category, required this.title, required this.subtitle});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Row(
        children: [
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              color: AppColors.surfaceVariant,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Icon(icon, color: AppColors.primary, size: 36),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(category,
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: AppColors.onSurfaceVariant,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 1.5,
                        )),
                const SizedBox(height: 4),
                Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 4),
                Text(subtitle,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

