import 'package:flutter/material.dart';
import '../../../core/theme/colors.dart';

class RoleBadge extends StatelessWidget {
  final String label;
  final Color? color;

  const RoleBadge({super.key, required this.label, this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: color ?? AppColors.secondaryFixed,
        borderRadius: BorderRadius.circular(9999),
      ),
      child: Text(
        label.toUpperCase(),
        style: Theme.of(context).textTheme.labelSmall?.copyWith(
              color: AppColors.onSecondaryContainer,
              fontWeight: FontWeight.w700,
              letterSpacing: 1,
            ),
      ),
    );
  }
}
