import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.darkNavy,
      body: Stack(
        children: [
          // Decorative gradient area
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            height: MediaQuery.of(context).size.height * 0.45,
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    AppColors.primaryContainer.withValues(alpha: 0.2),
                    Colors.transparent,
                  ],
                ),
              ),
              child: Stack(
                children: [
                  // Radial glow
                  Center(
                    child: Container(
                      width: 300,
                      height: 300,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        gradient: RadialGradient(
                          colors: [
                            AppColors.primaryContainer.withValues(alpha: 0.4),
                            Colors.transparent,
                          ],
                        ),
                      ),
                    ),
                  ),
                  // Nodes
                  Positioned(
                    top: MediaQuery.of(context).size.height * 0.08,
                    left: MediaQuery.of(context).size.width * 0.3,
                    child: Container(
                      width: 12,
                      height: 12,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.white,
                        boxShadow: [BoxShadow(color: Colors.white.withValues(alpha: 0.8), blurRadius: 15)],
                      ),
                    ),
                  ),
                  Positioned(
                    top: MediaQuery.of(context).size.height * 0.18,
                    left: MediaQuery.of(context).size.width * 0.6,
                    child: Container(
                      width: 16,
                      height: 16,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: AppColors.secondaryContainer,
                        boxShadow: [BoxShadow(color: AppColors.secondaryContainer.withValues(alpha: 0.8), blurRadius: 20)],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Main content
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  const Spacer(flex: 2),

                  // Header
                  Text(
                    'ResQ',
                    style: Theme.of(context).textTheme.displayMedium?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w800,
                          letterSpacing: -0.5,
                        ),
                  ).animate().fadeIn(duration: 600.ms).slideY(begin: 0.3),

                  const SizedBox(height: 16),

                  Text(
                    'Select your user type to continue',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: AppColors.surfaceVariant.withValues(alpha: 0.8),
                          letterSpacing: 0.5,
                        ),
                  ).animate().fadeIn(delay: 200.ms, duration: 600.ms),

                  const SizedBox(height: 48),

                  // Staff Card
                  _UserTypeCard(
                    icon: Icons.badge_outlined,
                    iconColor: AppColors.primary,
                    iconBgColor: AppColors.primaryContainer.withValues(alpha: 0.2),
                    title: "I'm a Staff Member",
                    subtitle: 'Access management tools, monitor alerts, and manage property settings.',
                    onTap: () => context.go('/staff/login'),
                  ).animate().fadeIn(delay: 400.ms, duration: 500.ms).slideY(begin: 0.2),

                  const SizedBox(height: 20),

                  // Guest Card
                  _UserTypeCard(
                    icon: Icons.luggage_outlined,
                    iconColor: AppColors.secondary,
                    iconBgColor: AppColors.secondaryContainer.withValues(alpha: 0.2),
                    title: "I'm a Guest",
                    subtitle: 'View emergency procedures, access building guides, and report issues.',
                    onTap: () => context.go('/guest/checkin'),
                  ).animate().fadeIn(delay: 550.ms, duration: 500.ms).slideY(begin: 0.2),

                  const Spacer(flex: 2),

                  // Language selector
                  Container(
                    padding: const EdgeInsets.all(4),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceContainerLow.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(9999),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        _LanguageChip(label: 'English', selected: true),
                        _LanguageChip(label: 'Español', selected: false),
                        _LanguageChip(label: 'Français', selected: false),
                      ],
                    ),
                  ).animate().fadeIn(delay: 700.ms),

                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _UserTypeCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final Color iconBgColor;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _UserTypeCard({
    required this.icon,
    required this.iconColor,
    required this.iconBgColor,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.surfaceContainerLow,
      borderRadius: BorderRadius.circular(20),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    width: 56,
                    height: 56,
                    decoration: BoxDecoration(shape: BoxShape.circle, color: iconBgColor),
                    child: Icon(icon, size: 28, color: iconColor),
                  ),
                  Icon(Icons.arrow_forward, color: AppColors.outline),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                title,
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 8),
              Text(
                subtitle,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: AppColors.onSurfaceVariant,
                      height: 1.5,
                    ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _LanguageChip extends StatelessWidget {
  final String label;
  final bool selected;

  const _LanguageChip({required this.label, required this.selected});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: selected ? AppColors.secondaryFixed : Colors.transparent,
        borderRadius: BorderRadius.circular(9999),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelSmall?.copyWith(
              color: selected ? AppColors.onSecondaryContainer : AppColors.onSurfaceVariant,
              fontWeight: FontWeight.w500,
            ),
      ),
    );
  }
}
