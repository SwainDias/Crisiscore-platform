import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/theme/colors.dart';
import '../../../providers.dart';

class GuestAccountTabScreen extends ConsumerWidget {
  const GuestAccountTabScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Account',
              style: Theme.of(context)
                  .textTheme
                  .headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 16),
            Card(
              child: ListTile(
                leading: const Icon(Icons.person_outline),
                title: Text(mockGuest.name),
                subtitle: Text('Room ${mockGuest.room}'),
              ),
            ),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                leading: const Icon(Icons.hotel_outlined),
                title: Text(mockGuest.hotel),
                subtitle: Text('${mockGuest.wing}, ${mockGuest.floor}'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
