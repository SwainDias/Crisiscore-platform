import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/colors.dart';

class TrainingDrillScreen extends StatefulWidget {
  final String drillId;
  const TrainingDrillScreen({super.key, required this.drillId});

  @override
  State<TrainingDrillScreen> createState() => _TrainingDrillScreenState();
}

class _TrainingDrillScreenState extends State<TrainingDrillScreen> {
  int _currentStep = 2;
  final int _totalSteps = 5;
  int? _selectedOption;
  bool _showFeedback = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () => context.pop(),
        ),
        title: Text('Micro-Drill',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.primary,
                  fontWeight: FontWeight.w700,
                )),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Center(
              child: Text('$_currentStep of $_totalSteps',
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(color: AppColors.onSurfaceVariant)),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Progress bar
          Container(
            height: 4,
            color: AppColors.surfaceContainerHighest,
            child: FractionallySizedBox(
              alignment: Alignment.centerLeft,
              widthFactor: _currentStep / _totalSteps,
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.horizontal(right: Radius.circular(9999)),
                  gradient: const LinearGradient(
                    colors: [AppColors.primary, AppColors.primaryContainer],
                  ),
                ),
              ),
            ),
          ),

          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  // Scenario image placeholder
                  Container(
                    height: 200,
                    decoration: BoxDecoration(
                      color: AppColors.surfaceContainerLow,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Stack(
                      children: [
                        Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                            gradient: LinearGradient(
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                              colors: [
                                AppColors.primaryContainer.withValues(alpha: 0.3),
                                AppColors.darkNavy.withValues(alpha: 0.8),
                              ],
                            ),
                          ),
                          child: Center(
                            child: Icon(Icons.dns, color: AppColors.primaryContainer.withValues(alpha: 0.5), size: 80),
                          ),
                        ),
                        Positioned(
                          bottom: 12,
                          left: 16,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppColors.secondaryFixed,
                              borderRadius: BorderRadius.circular(9999),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.warning, size: 14, color: AppColors.onSecondaryContainer),
                                const SizedBox(width: 6),
                                Text('Incident Response',
                                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                          color: AppColors.onSecondaryContainer,
                                          fontWeight: FontWeight.w600,
                                        )),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ).animate().fadeIn(),

                  const SizedBox(height: 24),

                  // Question
                  Text(
                    'You receive an alert for an unexpected traffic spike on Node Alpha.',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700, height: 1.3),
                  ).animate().fadeIn(delay: 100.ms),
                  const SizedBox(height: 8),
                  Text(
                    'What is the first immediate action required by the ResQ protocol?',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.onSurfaceVariant, height: 1.5),
                  ).animate().fadeIn(delay: 200.ms),

                  const SizedBox(height: 28),

                  // Options
                  _OptionButton(
                    index: 0,
                    text: 'Restart Node Alpha to clear connections.',
                    feedback: 'Incorrect. Restarting without investigation destroys potential forensic data.',
                    isCorrect: false,
                    isSelected: _selectedOption == 0,
                    showFeedback: _showFeedback && _selectedOption == 0,
                    onTap: () => _selectOption(0),
                  ).animate().fadeIn(delay: 300.ms),
                  const SizedBox(height: 12),
                  _OptionButton(
                    index: 1,
                    text: 'Isolate Node Alpha from the main load balancer.',
                    isCorrect: false,
                    isSelected: _selectedOption == 1,
                    showFeedback: false,
                    onTap: () => _selectOption(1),
                  ).animate().fadeIn(delay: 350.ms),
                  const SizedBox(height: 12),
                  _OptionButton(
                    index: 2,
                    text: 'Verify alert authenticity via the primary dashboard.',
                    feedback: 'Correct! Always confirm the alert is not a false positive before initiating structural changes.',
                    isCorrect: true,
                    isSelected: _selectedOption == 2,
                    showFeedback: _showFeedback && _selectedOption == 2,
                    onTap: () => _selectOption(2),
                  ).animate().fadeIn(delay: 400.ms),
                  const SizedBox(height: 12),
                  _OptionButton(
                    index: 3,
                    text: 'Notify the executive team immediately.',
                    isCorrect: false,
                    isSelected: _selectedOption == 3,
                    showFeedback: false,
                    onTap: () => _selectOption(3),
                  ).animate().fadeIn(delay: 450.ms),

                  const SizedBox(height: 32),

                  // Continue button
                  Align(
                    alignment: Alignment.centerRight,
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(9999),
                        gradient: const LinearGradient(
                          colors: [AppColors.primary, AppColors.primaryContainer],
                        ),
                        boxShadow: [
                          BoxShadow(color: AppColors.primary.withValues(alpha: 0.25), blurRadius: 24, offset: const Offset(0, 8)),
                        ],
                      ),
                      child: FilledButton(
                        onPressed: () {
                          if (_currentStep < _totalSteps) {
                            setState(() {
                              _currentStep++;
                              _selectedOption = null;
                              _showFeedback = false;
                            });
                          } else {
                            context.pop();
                          }
                        },
                        style: FilledButton.styleFrom(
                          backgroundColor: Colors.transparent,
                          shadowColor: Colors.transparent,
                          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text('Continue', style: TextStyle(fontWeight: FontWeight.w600)),
                            const SizedBox(width: 8),
                            const Icon(Icons.arrow_forward, size: 20),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _selectOption(int index) {
    setState(() {
      _selectedOption = index;
      _showFeedback = true;
    });
  }
}

class _OptionButton extends StatelessWidget {
  final int index;
  final String text;
  final String? feedback;
  final bool isCorrect;
  final bool isSelected;
  final bool showFeedback;
  final VoidCallback onTap;

  const _OptionButton({
    required this.index,
    required this.text,
    this.feedback,
    required this.isCorrect,
    required this.isSelected,
    required this.showFeedback,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    Color borderColor = AppColors.outlineVariant;
    Color bgColor = AppColors.surfaceContainerLowest;

    if (isSelected && isCorrect) {
      borderColor = AppColors.primary;
      bgColor = AppColors.primary.withValues(alpha: 0.05);
    } else if (isSelected && !isCorrect) {
      borderColor = AppColors.error.withValues(alpha: 0.2);
    }

    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(12),
          border: isSelected ? Border.all(color: borderColor, width: 2) : null,
          boxShadow: [
            BoxShadow(color: AppColors.onSurface.withValues(alpha: 0.02), blurRadius: 20, offset: const Offset(0, 4)),
          ],
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 24,
              height: 24,
              margin: const EdgeInsets.only(top: 2),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: isSelected
                      ? (isCorrect ? AppColors.primary : AppColors.error)
                      : AppColors.outlineVariant,
                  width: 2,
                ),
                color: isSelected
                    ? (isCorrect ? AppColors.primary : AppColors.errorContainer)
                    : Colors.transparent,
              ),
              child: isSelected
                  ? Icon(
                      isCorrect ? Icons.check : Icons.close,
                      size: 14,
                      color: isCorrect ? Colors.white : AppColors.error,
                    )
                  : null,
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(text, style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.w500)),
                  if (showFeedback && feedback != null) ...[
                    const SizedBox(height: 8),
                    Text(feedback!,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: isCorrect ? AppColors.primary : AppColors.error.withValues(alpha: 0.8),
                            )),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
