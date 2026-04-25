import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';

class RoleConfirmationScreen extends StatelessWidget {
  const RoleConfirmationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primaryFixedDim,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Check circle
                Container(
                  width: 96,
                  height: 96,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.surfaceContainerLowest,
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.onSurface.withValues(alpha: 0.06),
                        blurRadius: 40,
                        offset: const Offset(0, 20),
                      ),
                    ],
                  ),
                  child: const Icon(Icons.check_circle, color: AppColors.primary, size: 56),
                ).animate().fadeIn(duration: 500.ms).scale(begin: const Offset(0.5, 0.5)),

                const SizedBox(height: 24),

                // Welcome text
                RichText(
                  textAlign: TextAlign.center,
                  text: TextSpan(
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                          fontWeight: FontWeight.w700,
                          height: 1.2,
                        ),
                    children: [
                      const TextSpan(text: 'Welcome back,\n'),
                      TextSpan(
                        text: mockStaff.name,
                        style: const TextStyle(color: AppColors.primary),
                      ),
                    ],
                  ),
                ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2),

                const SizedBox(height: 32),

                // Info card
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceContainerLowest,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.onSurface.withValues(alpha: 0.06),
                        blurRadius: 40,
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      // Top gradient bar
                      Container(
                        height: 4,
                        margin: const EdgeInsets.only(bottom: 20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(2),
                          gradient: const LinearGradient(
                            colors: [AppColors.primary, AppColors.primaryContainer],
                          ),
                        ),
                      ),

                      // Role
                      Text(
                        'CONFIRMED ROLE',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: AppColors.outline,
                              letterSpacing: 2,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        mockStaff.roleName,
                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700),
                      ),

                      const SizedBox(height: 24),

                      // System checks
                      Text(
                        'SYSTEM CHECKS',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: AppColors.outline,
                              letterSpacing: 2,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                      const SizedBox(height: 16),

                      _SystemCheckRow(icon: Icons.badge, label: 'PMS Connection', status: 'Active'),
                      const SizedBox(height: 12),
                      _SystemCheckRow(icon: Icons.my_location, label: 'GPS Tracking', status: 'Active'),
                      const SizedBox(height: 12),
                      _SystemCheckRow(icon: Icons.radio, label: 'Radio Freq', status: 'Synced'),
                    ],
                  ),
                ).animate().fadeIn(delay: 500.ms).slideY(begin: 0.1),

                const SizedBox(height: 32),

                // Enter button
                SizedBox(
                  width: double.infinity,
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(9999),
                      gradient: const LinearGradient(
                        colors: [AppColors.primary, AppColors.primaryContainer],
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primary.withValues(alpha: 0.2),
                          blurRadius: 40,
                          offset: const Offset(0, 20),
                        ),
                      ],
                    ),
                    child: FilledButton(
                      onPressed: () => context.go('/staff/home'),
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.transparent,
                        shadowColor: Colors.transparent,
                        padding: const EdgeInsets.symmetric(vertical: 20),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text('Enter ResQ', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
                          const SizedBox(width: 8),
                          const Icon(Icons.arrow_forward),
                        ],
                      ),
                    ),
                  ),
                ).animate().fadeIn(delay: 700.ms),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _SystemCheckRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String status;

  const _SystemCheckRow({required this.icon, required this.label, required this.status});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primary, size: 22),
          const SizedBox(width: 12),
          Expanded(
            child: Text(label, style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.w500)),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: AppColors.secondaryFixed,
              borderRadius: BorderRadius.circular(9999),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: const BoxDecoration(shape: BoxShape.circle, color: AppColors.primary),
                ),
                const SizedBox(width: 6),
                Text(
                  status.toUpperCase(),
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: AppColors.onSecondaryContainer,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 1,
                      ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
