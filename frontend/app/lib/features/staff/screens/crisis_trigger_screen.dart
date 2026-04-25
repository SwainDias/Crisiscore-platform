import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../providers.dart';
import '../../shared/widgets/hold_to_confirm_button.dart';

class CrisisTriggerScreen extends ConsumerStatefulWidget {
  const CrisisTriggerScreen({super.key});

  @override
  ConsumerState<CrisisTriggerScreen> createState() => _CrisisTriggerScreenState();
}

class _CrisisTriggerScreenState extends ConsumerState<CrisisTriggerScreen> {
  String? _selectedType;
  final _detailsController = TextEditingController();

  @override
  void dispose() {
    _detailsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
        title: Text('Raise an Alert',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Emergency Type',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 8),
                  Text('Select the nature of your crisis to notify responders immediately.',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant)),

                  const SizedBox(height: 24),

                  // Emergency type cards
                  _EmergencyTypeCard(
                    icon: Icons.local_fire_department,
                    title: 'Fire',
                    subtitle: 'Smoke or active flames',
                    bgColor: AppColors.errorContainer,
                    iconColor: AppColors.error,
                    selected: _selectedType == 'fire',
                    onTap: () => setState(() => _selectedType = 'fire'),
                  ).animate().fadeIn(delay: 100.ms),

                  const SizedBox(height: 16),

                  _EmergencyTypeCard(
                    icon: Icons.medical_services,
                    title: 'Medical',
                    subtitle: 'Injury, illness, or health crisis',
                    bgColor: AppColors.surfaceContainerLow,
                    iconColor: AppColors.onSecondaryContainer,
                    iconBgColor: AppColors.secondaryContainer,
                    selected: _selectedType == 'medical',
                    onTap: () => setState(() => _selectedType = 'medical'),
                  ).animate().fadeIn(delay: 200.ms),

                  const SizedBox(height: 16),

                  _EmergencyTypeCard(
                    icon: Icons.security,
                    title: 'Security',
                    subtitle: 'Intruder, threat, or unsafe situation',
                    bgColor: AppColors.surfaceContainerLow,
                    iconColor: AppColors.onTertiary,
                    iconBgColor: AppColors.tertiaryContainer,
                    selected: _selectedType == 'security',
                    onTap: () => setState(() => _selectedType = 'security'),
                  ).animate().fadeIn(delay: 300.ms),

                  const SizedBox(height: 24),

                  // Additional details
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceContainerLowest,
                      borderRadius: BorderRadius.circular(12),
                      boxShadow: [
                        BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.06), blurRadius: 40),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Additional Details (Optional)',
                            style: Theme.of(context).textTheme.labelLarge?.copyWith(fontWeight: FontWeight.w700)),
                        const SizedBox(height: 12),
                        TextField(
                          controller: _detailsController,
                          maxLines: 3,
                          decoration: const InputDecoration(
                            hintText: 'Location details, number of people involved...',
                          ),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(delay: 400.ms),
                ],
              ),
            ),
          ),

          // Bottom action
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.bottomCenter,
                end: Alignment.topCenter,
                colors: [AppColors.surface, AppColors.surface.withValues(alpha: 0)],
              ),
            ),
            child: HoldToConfirmButton(
              label: 'Hold to Send Alert',
              icon: Icons.campaign,
              onConfirmed: () {
                ref.read(activeIncidentProvider.notifier).setActive(true);
                Future.delayed(const Duration(milliseconds: 500), () {
                  if (context.mounted) context.pop();
                });
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _EmergencyTypeCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color bgColor;
  final Color iconColor;
  final Color? iconBgColor;
  final bool selected;
  final VoidCallback onTap;

  const _EmergencyTypeCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.bgColor,
    required this.iconColor,
    this.iconBgColor,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(20),
          border: selected ? Border.all(color: AppColors.primary, width: 2) : null,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: iconBgColor ?? Colors.white.withValues(alpha: 0.3),
              ),
              child: Icon(icon, size: 28, color: iconColor),
            ),
            const SizedBox(height: 16),
            Text(title, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 4),
            Text(subtitle, style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
          ],
        ),
      ),
    );
  }
}
