import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../core/constants/app_constants.dart';
import '../../../providers.dart';

class GuestCheckinScreen extends ConsumerStatefulWidget {
  const GuestCheckinScreen({super.key});

  @override
  ConsumerState<GuestCheckinScreen> createState() => _GuestCheckinScreenState();
}

class _GuestCheckinScreenState extends ConsumerState<GuestCheckinScreen> {
  String? _selectedBloodType;
  final Set<String> _selectedNeeds = {'Wheelchair Access'};
  bool _shareProfile = true;
  final _allergiesController = TextEditingController();

  @override
  void dispose() {
    _allergiesController.dispose();
    super.dispose();
  }

  Future<void> _continue() async {
    final prefs = ref.read(sharedPreferencesProvider);
    await prefs.setString(AppConstants.userTypeKey, AppConstants.guestType);
    ref.read(userTypeProvider.notifier).set(AppConstants.guestType);
    if (mounted) context.go('/guest/home');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          // App bar
          SliverAppBar(
            pinned: true,
            backgroundColor: AppColors.surfaceContainerLowest.withValues(alpha: 0.7),
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
              TextButton(
                onPressed: _continue,
                child: Text('Skip', style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.w600)),
              ),
            ],
          ),

          SliverPadding(
            padding: const EdgeInsets.all(24),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // Header
                Text(
                  'Guest Check-In',
                  style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.w800),
                ).animate().fadeIn(duration: 400.ms),
                const SizedBox(height: 8),
                Text(
                  'Please confirm your details for emergency preparedness.',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant, height: 1.5),
                ).animate().fadeIn(delay: 100.ms),

                const SizedBox(height: 32),

                // Room card
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceContainerLow,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(Icons.bed, color: AppColors.primary, size: 20),
                                const SizedBox(width: 8),
                                Text('ROOM ASSIGNMENT',
                                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                          color: AppColors.primary,
                                          fontWeight: FontWeight.w700,
                                          letterSpacing: 1.5,
                                        )),
                              ],
                            ),
                            const SizedBox(height: 12),
                            Text('Room ${mockGuest.room}',
                                style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w700)),
                            const SizedBox(height: 4),
                            Text('${mockGuest.wing}, ${mockGuest.floor}',
                                style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.onSurfaceVariant)),
                          ],
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: const BoxDecoration(
                          shape: BoxShape.circle,
                          color: AppColors.surfaceContainerLowest,
                        ),
                        child: const Icon(Icons.check_circle, color: AppColors.secondary, size: 24),
                      ),
                    ],
                  ),
                ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.1),

                const SizedBox(height: 32),

                // Emergency profile header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Emergency Profile',
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
                        const SizedBox(height: 4),
                        Text('Information shared securely with responders.',
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant)),
                      ],
                    ),
                    Row(
                      children: [
                        Switch(
                          value: _shareProfile,
                          onChanged: (v) => setState(() => _shareProfile = v),
                          activeThumbColor: AppColors.primary,
                        ),
                      ],
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // Blood type
                Text('Blood Type', style: Theme.of(context).textTheme.labelLarge),
                const SizedBox(height: 8),
                DropdownButtonFormField<String>(
                  initialValue: _selectedBloodType,
                  decoration: const InputDecoration(hintText: 'Select blood type'),
                  items: ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-', 'Unknown']
                      .map((t) => DropdownMenuItem(value: t, child: Text(t)))
                      .toList(),
                  onChanged: (v) => setState(() => _selectedBloodType = v),
                ),

                const SizedBox(height: 24),

                // Mobility needs
                Text('Mobility & Assistance Needs', style: Theme.of(context).textTheme.labelLarge),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    _NeedChip(icon: Icons.accessible, label: 'Wheelchair Access', selected: _selectedNeeds.contains('Wheelchair Access'), onTap: () => _toggleNeed('Wheelchair Access')),
                    _NeedChip(icon: Icons.hearing, label: 'Hearing Impaired', selected: _selectedNeeds.contains('Hearing Impaired'), onTap: () => _toggleNeed('Hearing Impaired')),
                    _NeedChip(icon: Icons.visibility, label: 'Visually Impaired', selected: _selectedNeeds.contains('Visually Impaired'), onTap: () => _toggleNeed('Visually Impaired')),
                    _NeedChip(icon: Icons.pets, label: 'Service Animal', selected: _selectedNeeds.contains('Service Animal'), onTap: () => _toggleNeed('Service Animal')),
                  ],
                ),

                const SizedBox(height: 24),

                // Allergies
                Text('Medical Allergies or Notes', style: Theme.of(context).textTheme.labelLarge),
                const SizedBox(height: 8),
                TextField(
                  controller: _allergiesController,
                  maxLines: 3,
                  decoration: const InputDecoration(
                    hintText: 'List any medications or conditions...',
                  ),
                ),

                const SizedBox(height: 40),

                // Continue button
                Align(
                  alignment: Alignment.centerRight,
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(9999),
                      gradient: const LinearGradient(
                        colors: [AppColors.primary, AppColors.primaryContainer],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                    ),
                    child: FilledButton(
                      onPressed: _continue,
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.transparent,
                        shadowColor: Colors.transparent,
                        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 18),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Text('Continue', style: TextStyle(fontWeight: FontWeight.w700)),
                          const SizedBox(width: 8),
                          const Icon(Icons.arrow_forward, size: 20),
                        ],
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 32),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  void _toggleNeed(String need) {
    setState(() {
      if (_selectedNeeds.contains(need)) {
        _selectedNeeds.remove(need);
      } else {
        _selectedNeeds.add(need);
      }
    });
  }
}

class _NeedChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _NeedChip({required this.icon, required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: selected ? AppColors.secondaryFixed : AppColors.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(9999),
          border: selected ? null : Border.all(color: AppColors.outlineVariant.withValues(alpha: 0.15)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 18, color: selected ? AppColors.onSecondaryContainer : AppColors.onSurface),
            const SizedBox(width: 8),
            Text(label, style: Theme.of(context).textTheme.labelMedium?.copyWith(fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}
