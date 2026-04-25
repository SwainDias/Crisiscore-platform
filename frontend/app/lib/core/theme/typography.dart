import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTypography {
  static TextTheme get textTheme {
    final headlineFont = GoogleFonts.plusJakartaSans();
    final bodyFont = GoogleFonts.inter();

    return TextTheme(
      displayLarge: headlineFont.copyWith(fontSize: 56, fontWeight: FontWeight.w800, letterSpacing: -0.5),
      displayMedium: headlineFont.copyWith(fontSize: 44, fontWeight: FontWeight.w700, letterSpacing: -0.3),
      displaySmall: headlineFont.copyWith(fontSize: 36, fontWeight: FontWeight.w700),
      headlineLarge: headlineFont.copyWith(fontSize: 32, fontWeight: FontWeight.w700),
      headlineMedium: headlineFont.copyWith(fontSize: 28, fontWeight: FontWeight.w700),
      headlineSmall: headlineFont.copyWith(fontSize: 24, fontWeight: FontWeight.w700),
      titleLarge: headlineFont.copyWith(fontSize: 22, fontWeight: FontWeight.w600),
      titleMedium: headlineFont.copyWith(fontSize: 16, fontWeight: FontWeight.w600, letterSpacing: 0.15),
      titleSmall: headlineFont.copyWith(fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.1),
      bodyLarge: bodyFont.copyWith(fontSize: 16, fontWeight: FontWeight.w400, letterSpacing: 0.15),
      bodyMedium: bodyFont.copyWith(fontSize: 14, fontWeight: FontWeight.w400, letterSpacing: 0.25),
      bodySmall: bodyFont.copyWith(fontSize: 12, fontWeight: FontWeight.w400, letterSpacing: 0.4),
      labelLarge: bodyFont.copyWith(fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.1),
      labelMedium: bodyFont.copyWith(fontSize: 12, fontWeight: FontWeight.w600, letterSpacing: 0.5),
      labelSmall: bodyFont.copyWith(fontSize: 11, fontWeight: FontWeight.w600, letterSpacing: 0.5),
    );
  }
}
