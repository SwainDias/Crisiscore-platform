import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';
import '../../../core/constants/app_constants.dart';
import '../../../providers.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);

    Future.delayed(AppConstants.splashDuration, () {
      if (!mounted) {
        return;
      }

      final userType = ref.read(userTypeProvider);
      if (userType == AppConstants.staffType) {
        context.go('/staff/home');
      } else if (userType == AppConstants.guestType) {
        context.go('/guest/home');
      } else {
        context.go('/onboarding');
      }
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.darkNavy,
      body: Stack(
        children: [
          // Ambient glows
          Positioned(
            top: MediaQuery.of(context).size.height * 0.25,
            left: MediaQuery.of(context).size.width * 0.15,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.primaryContainer.withValues(alpha: 0.2),
              ),
            ),
          ),
          Positioned(
            bottom: MediaQuery.of(context).size.height * 0.2,
            right: MediaQuery.of(context).size.width * 0.1,
            child: Container(
              width: 400,
              height: 400,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.secondaryContainer.withValues(alpha: 0.1),
              ),
            ),
          ),

          // Center content
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Pulse rings + Shield
                SizedBox(
                  width: 128,
                  height: 128,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      AnimatedBuilder(
                        animation: _pulseController,
                        builder: (context, child) {
                          return Transform.scale(
                            scale: 1.5 + _pulseController.value * 0.3,
                            child: Container(
                              width: 96,
                              height: 96,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: AppColors.primaryContainer.withValues(alpha: 0.3 - _pulseController.value * 0.15),
                                  width: 2,
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                      AnimatedBuilder(
                        animation: _pulseController,
                        builder: (context, child) {
                          return Transform.scale(
                            scale: 2.0 + _pulseController.value * 0.2,
                            child: Container(
                              width: 96,
                              height: 96,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: AppColors.secondaryContainer.withValues(alpha: 0.2 - _pulseController.value * 0.1),
                                  width: 1,
                                ),
                              ),
                            ),
                          );
                        },
                      ),
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
                              color: AppColors.primaryContainer.withValues(alpha: 0.4),
                              blurRadius: 40,
                            ),
                          ],
                        ),
                        child: const Icon(Icons.shield_rounded, color: Colors.white, size: 48),
                      ),
                    ],
                  ),
                ).animate().fadeIn(duration: 600.ms).scale(begin: const Offset(0.8, 0.8)),

                const SizedBox(height: 32),

                // Title
                Text(
                  AppConstants.appName,
                  style: Theme.of(context).textTheme.displaySmall?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w800,
                        letterSpacing: -0.5,
                      ),
                ).animate().fadeIn(delay: 300.ms, duration: 600.ms).slideY(begin: 0.2),

                const SizedBox(height: 12),

                Text(
                  AppConstants.tagline,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: AppColors.primaryFixedDim,
                        fontWeight: FontWeight.w500,
                        letterSpacing: 1,
                      ),
                ).animate().fadeIn(delay: 500.ms, duration: 600.ms),

                const SizedBox(height: 64),

                // Loading bar
                SizedBox(
                  width: 200,
                  height: 4,
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(9999),
                    child: LinearProgressIndicator(
                      backgroundColor: AppColors.surfaceContainer.withValues(alpha: 0.1),
                      valueColor: const AlwaysStoppedAnimation(AppColors.primaryContainer),
                    ),
                  ),
                ).animate().fadeIn(delay: 700.ms),

                const SizedBox(height: 16),

                Text(
                  'Initializing systems...',
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: AppColors.outlineVariant.withValues(alpha: 0.7),
                      ),
                ).animate().fadeIn(delay: 800.ms),
              ],
            ),
          ),

          // Footer
          Positioned(
            bottom: 32,
            left: 0,
            right: 0,
            child: Text(
              AppConstants.poweredBy.toUpperCase(),
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: AppColors.surfaceVariant.withValues(alpha: 0.5),
                    letterSpacing: 2,
                  ),
            ).animate().fadeIn(delay: 1000.ms),
          ),
        ],
      ),
    );
  }
}
