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
      floatingActionButton: Container(
        width: 64,
        height: 64,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: const LinearGradient(
            colors: [AppColors.primary, AppColors.primaryContainer],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          boxShadow: [
            BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.15), blurRadius: 40, offset: const Offset(0, 10)),
          ],
        ),
        child: FloatingActionButton(
          onPressed: () {},
          backgroundColor: Colors.transparent,
          elevation: 0,
          child: const Icon(Icons.sos, color: Colors.white, size: 32),
        ),
      ),
      body: CustomScrollView(
        slivers: [
          // App bar
          SliverAppBar(
            pinned: true,
            floating: true,
            backgroundColor: AppColors.surface.withValues(alpha: 0.7),
            automaticallyImplyLeading: false,
            title: Text('Emergency Response',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            leading: IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {},
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

          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                const SizedBox(height: 8),

                // Welcome hero
                RichText(
                  text: TextSpan(
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.w700, height: 1.2),
                    children: [
                      const TextSpan(text: 'Stay Safe,\n'),
                      TextSpan(
                        text: '${mockGuest.name}.',
                        style: TextStyle(
                          foreground: Paint()
                            ..shader = const LinearGradient(
                              colors: [AppColors.primary, AppColors.primaryContainer],
                            ).createShader(const Rect.fromLTWH(0, 0, 200, 50)),
                        ),
                      ),
                    ],
                  ),
                ).animate().fadeIn(duration: 500.ms),

                const SizedBox(height: 12),
                Text(
                  'You are currently checked into ${mockGuest.hotel}. Your safety is our priority.',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant, height: 1.5),
                ).animate().fadeIn(delay: 100.ms),

                const SizedBox(height: 24),

                // Active alert card
                if (hasActive)
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: AppColors.errorContainer,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(color: AppColors.error.withValues(alpha: 0.1), blurRadius: 40, offset: const Offset(0, 20)),
                      ],
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 56,
                          height: 56,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: AppColors.error,
                            boxShadow: [BoxShadow(color: AppColors.error.withValues(alpha: 0.2), blurRadius: 20)],
                          ),
                          child: const Icon(Icons.campaign, color: Colors.white, size: 28),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Text('ACTIVE ALERT',
                                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                            color: AppColors.error,
                                            fontWeight: FontWeight.w700,
                                            letterSpacing: 1.5,
                                          )),
                                  const SizedBox(width: 8),
                                  const PulseIndicator(color: AppColors.error, size: 6),
                                ],
                              ),
                              const SizedBox(height: 8),
                              Text('Severe Weather Warning',
                                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                        color: AppColors.onErrorContainer,
                                        fontWeight: FontWeight.w700,
                                      )),
                              const SizedBox(height: 8),
                              Text(
                                'A severe thunderstorm warning has been issued. Please remain indoors.',
                                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                      color: AppColors.onErrorContainer.withValues(alpha: 0.9),
                                      height: 1.4,
                                    ),
                              ),
                              const SizedBox(height: 16),
                              SizedBox(
                                width: double.infinity,
                                child: FilledButton(
                                  onPressed: () => context.push('/guest/instructions'),
                                  style: FilledButton.styleFrom(
                                    backgroundColor: AppColors.error,
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(vertical: 14),
                                  ),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      const Text('View Details'),
                                      const SizedBox(width: 8),
                                      const Icon(Icons.arrow_forward, size: 18),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.1),

                const SizedBox(height: 28),

                // Quick Actions
                Text('Quick Actions',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 16),

                SizedBox(
                  height: 200,
                  child: ListView(
                    scrollDirection: Axis.horizontal,
                    children: [
                      _ActionCard(
                        icon: Icons.phone_in_talk,
                        iconColor: AppColors.primary,
                        title: 'Call for Help',
                        subtitle: 'Connect with emergency services or hotel security.',
                      ).animate().fadeIn(delay: 300.ms),
                      const SizedBox(width: 12),
                      _ActionCard(
                        icon: Icons.meeting_room,
                        iconColor: AppColors.onSecondaryContainer,
                        iconBg: AppColors.secondaryContainer.withValues(alpha: 0.3),
                        title: 'Exit Routes',
                        subtitle: 'View the fastest evacuation paths from your room.',
                      ).animate().fadeIn(delay: 350.ms),
                      const SizedBox(width: 12),
                      _ActionCard(
                        icon: Icons.verified_user,
                        iconColor: AppColors.tertiary,
                        iconBg: AppColors.tertiaryContainer.withValues(alpha: 0.2),
                        title: 'Safe Zones',
                        subtitle: 'Locate designated assembly areas.',
                      ).animate().fadeIn(delay: 400.ms),
                    ],
                  ),
                ),

                const SizedBox(height: 28),

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
                          Text('See All', style: TextStyle(color: AppColors.primary)),
                          const Icon(Icons.arrow_forward, size: 14, color: AppColors.primary),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                _InfoHubCard(icon: Icons.fire_extinguisher, category: 'PROTOCOL', title: 'Fire Safety Procedures',
                    subtitle: 'Review what to do in case of a fire alarm.').animate().fadeIn(delay: 500.ms),
                const SizedBox(height: 12),
                _InfoHubCard(icon: Icons.health_and_safety, category: 'RESOURCES', title: 'First Aid Locations',
                    subtitle: 'Find nearby medical kits and AEDs.').animate().fadeIn(delay: 550.ms),

                const SizedBox(height: 80),
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
      width: 200,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.outlineVariant.withValues(alpha: 0.15)),
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
          const Spacer(),
          Text(title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 4),
          Text(subtitle,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
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
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.outlineVariant.withValues(alpha: 0.15)),
      ),
      child: Row(
        children: [
          Container(
            width: 64,
            height: 64,
            decoration: BoxDecoration(
              color: AppColors.surfaceVariant,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: AppColors.primary, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(category,
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: AppColors.onSurfaceVariant,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 1.5,
                        )),
                const SizedBox(height: 4),
                Text(title, style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 2),
                Text(subtitle,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
