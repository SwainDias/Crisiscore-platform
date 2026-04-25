import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../../core/theme/colors.dart';

class SilentPanicScreen extends StatelessWidget {
  const SilentPanicScreen({super.key});

  void _triggerSilentAlert(BuildContext context) {
    HapticFeedback.lightImpact();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('✓', textAlign: TextAlign.center,
            style: TextStyle(fontSize: 18, color: AppColors.safeGreen)),
        backgroundColor: AppColors.surfaceContainerLowest,
        duration: const Duration(seconds: 1),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        width: 60,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.surfaceContainerLowest.withValues(alpha: 0.7),
        leading: Padding(
          padding: const EdgeInsets.all(8),
          child: GestureDetector(
            onLongPress: () => _triggerSilentAlert(context),
            child: Container(
              decoration: const BoxDecoration(shape: BoxShape.circle),
              child: const Icon(Icons.emergency, color: AppColors.primary),
            ),
          ),
        ),
        title: Text('ResQ',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.primary,
                  fontWeight: FontWeight.w800,
                )),
        actions: [
          Padding(
            padding: const EdgeInsets.all(8),
            child: CircleAvatar(
              backgroundColor: AppColors.surfaceContainerHigh,
              child: const Icon(Icons.person, color: AppColors.onSurfaceVariant, size: 20),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Staff Safety Check',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            Text('Routine status verification. Tap elements to review current shift details.',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant)),

            const SizedBox(height: 28),

            _StatusRow(icon: Icons.location_on, title: 'Current Zone', value: 'Sector 4 - Alpha')
                .animate().fadeIn(delay: 100.ms).slideX(begin: -0.05),
            const SizedBox(height: 16),
            _StatusRow(icon: Icons.schedule, title: 'Shift Status', value: 'Active - 04:22 elapsed')
                .animate().fadeIn(delay: 200.ms).slideX(begin: -0.05),
            const SizedBox(height: 16),
            _StatusRow(icon: Icons.battery_5_bar, title: 'Device Status', value: 'Optimal - 87%')
                .animate().fadeIn(delay: 300.ms).slideX(begin: -0.05),

            // Hidden panic area - very subtle
            const SizedBox(height: 48),
            GestureDetector(
              onLongPress: () => _triggerSilentAlert(context),
              child: Center(
                child: Opacity(
                  opacity: 0.0,
                  child: Text('System Diagnostic',
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: AppColors.onSurfaceVariant,
                            letterSpacing: 2,
                          )),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StatusRow extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;

  const _StatusRow({required this.icon, required this.title, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: const BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.secondaryContainer,
            ),
            child: Icon(icon, color: AppColors.onSecondaryContainer),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 4),
                Text(value,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
              ],
            ),
          ),
          Icon(Icons.chevron_right, color: AppColors.outline),
        ],
      ),
    );
  }
}
