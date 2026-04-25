import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/colors.dart';
import '../../../core/constants/app_constants.dart';
import '../../../providers.dart';

class StaffLoginScreen extends ConsumerStatefulWidget {
  const StaffLoginScreen({super.key});

  @override
  ConsumerState<StaffLoginScreen> createState() => _StaffLoginScreenState();
}

class _StaffLoginScreenState extends ConsumerState<StaffLoginScreen> {
  final _empIdController = TextEditingController();
  final _pinController = TextEditingController();
  bool _useBiometrics = false;

  @override
  void dispose() {
    _empIdController.dispose();
    _pinController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    final prefs = ref.read(sharedPreferencesProvider);
    await prefs.setString(AppConstants.userTypeKey, AppConstants.staffType);
    ref.read(userTypeProvider.notifier).set(AppConstants.staffType);
    if (mounted) context.go('/staff/role-confirm');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surfaceContainerLow,
      body: Stack(
        children: [
          // Background glows
          Positioned(
            top: -200,
            right: -100,
            child: Container(
              width: 400,
              height: 400,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.primaryFixed.withValues(alpha: 0.2),
              ),
            ),
          ),
          Positioned(
            bottom: -150,
            left: -50,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.secondaryFixed.withValues(alpha: 0.2),
              ),
            ),
          ),

          SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const SizedBox(height: 40),

                  // Logo
                  Container(
                    width: 96,
                    height: 96,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: const LinearGradient(
                        colors: [AppColors.primary, AppColors.primaryContainer],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primary.withValues(alpha: 0.2),
                          blurRadius: 40,
                          offset: const Offset(0, 20),
                        ),
                      ],
                    ),
                    child: const Icon(Icons.emergency, color: Colors.white, size: 48),
                  ).animate().fadeIn(duration: 500.ms).scale(begin: const Offset(0.8, 0.8)),

                  const SizedBox(height: 16),

                  Text(
                    'ResQ',
                    style: Theme.of(context).textTheme.displaySmall?.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.w800,
                          letterSpacing: -0.5,
                        ),
                  ).animate().fadeIn(delay: 200.ms),
                  const SizedBox(height: 4),
                  Text(
                    'Staff Portal Access',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant),
                  ).animate().fadeIn(delay: 300.ms),

                  const SizedBox(height: 32),

                  // Detection card
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceContainerHigh,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      children: [
                        Container(
                          width: 48,
                          height: 48,
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            color: AppColors.secondaryFixed,
                          ),
                          child: const Icon(Icons.location_on, color: AppColors.onSecondaryContainer),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Secure Property Detected',
                                  style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w700)),
                              const SizedBox(height: 4),
                              Text(
                                'Connecting to ResQ HQ internal network.',
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.onSurfaceVariant),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.1),

                  const SizedBox(height: 24),

                  // Login form
                  Container(
                    padding: const EdgeInsets.all(28),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceContainerLowest,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.onSurface.withValues(alpha: 0.06),
                          blurRadius: 60,
                          offset: const Offset(0, 20),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        // Employee ID
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Employee ID',
                                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                                      color: AppColors.onSurfaceVariant,
                                      fontWeight: FontWeight.w600,
                                    )),
                            const SizedBox(height: 8),
                            TextField(
                              controller: _empIdController,
                              decoration: InputDecoration(
                                prefixIcon: const Icon(Icons.badge_outlined, color: AppColors.outline),
                                hintText: 'e.g. RQ-8842',
                                hintStyle: TextStyle(color: AppColors.outline),
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 20),

                        // PIN
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Secure PIN',
                                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                                      color: AppColors.onSurfaceVariant,
                                      fontWeight: FontWeight.w600,
                                    )),
                            const SizedBox(height: 8),
                            TextField(
                              controller: _pinController,
                              obscureText: true,
                              decoration: InputDecoration(
                                prefixIcon: const Icon(Icons.dialpad, color: AppColors.outline),
                                hintText: '••••••',
                                hintStyle: TextStyle(color: AppColors.outline, letterSpacing: 4),
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 24),

                        // Biometric toggle
                        Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: AppColors.surfaceContainerLow,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.fingerprint, color: AppColors.primary),
                              const SizedBox(width: 12),
                              Text('Use Biometrics',
                                  style: Theme.of(context).textTheme.labelLarge?.copyWith(fontWeight: FontWeight.w500)),
                              const Spacer(),
                              Switch(
                                value: _useBiometrics,
                                onChanged: (v) => setState(() => _useBiometrics = v),
                                activeThumbColor: AppColors.primary,
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 28),

                        // Sign in button
                        SizedBox(
                          width: double.infinity,
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(9999),
                              gradient: const LinearGradient(
                                colors: [AppColors.primary, AppColors.primaryContainer],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: AppColors.primary.withValues(alpha: 0.2),
                                  blurRadius: 20,
                                  offset: const Offset(0, 10),
                                ),
                              ],
                            ),
                            child: FilledButton(
                              onPressed: _login,
                              style: FilledButton.styleFrom(
                                backgroundColor: Colors.transparent,
                                shadowColor: Colors.transparent,
                                padding: const EdgeInsets.symmetric(vertical: 18),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Text('Sign In', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                                  const SizedBox(width: 8),
                                  const Icon(Icons.arrow_forward, size: 20),
                                ],
                              ),
                            ),
                          ),
                        ),

                        const SizedBox(height: 12),

                        TextButton(
                          onPressed: () {},
                          child: Text('Recover Credentials',
                              style: Theme.of(context).textTheme.labelMedium?.copyWith(color: AppColors.primary)),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(delay: 500.ms).slideY(begin: 0.1),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
