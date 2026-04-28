import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../../../core/theme/colors.dart';

class ResQMapWidget extends StatefulWidget {
  final bool interactive;
  final bool showIncidentPin;
  final bool showStaffDots;
  final bool showEvacRoute;

  const ResQMapWidget({
    super.key,
    this.interactive = true,
    this.showIncidentPin = false,
    this.showStaffDots = false,
    this.showEvacRoute = false,
  });

  @override
  State<ResQMapWidget> createState() => _ResQMapWidgetState();
}

class _ResQMapWidgetState extends State<ResQMapWidget> {
  static const _center = LatLng(19.0760, 72.8777);

  @override
  Widget build(BuildContext context) {
    final List<Marker> markers = [];

    if (widget.showIncidentPin) {
      markers.add(
        const Marker(
          point: LatLng(19.0767, 72.8780),
          width: 40,
          height: 40,
          child: Icon(Icons.location_on, color: AppColors.error, size: 40),
        ),
      );
    }

    if (widget.showStaffDots) {
      markers.addAll([
        const Marker(
          point: LatLng(19.0758, 72.8769),
          width: 24,
          height: 24,
          child: _StaffDot(),
        ),
        const Marker(
          point: LatLng(19.0762, 72.8775),
          width: 24,
          height: 24,
          child: _StaffDot(),
        ),
        const Marker(
          point: LatLng(19.0764, 72.8786),
          width: 24,
          height: 24,
          child: _StaffDot(),
        ),
      ]);
    }

    final List<Polyline> polylines = [];
    if (widget.showEvacRoute) {
      polylines.add(
        Polyline(
          points: const [
            LatLng(19.0757, 72.8768),
            LatLng(19.0761, 72.8774),
            LatLng(19.0764, 72.8779),
            LatLng(19.0768, 72.8785),
          ],
          strokeWidth: 5,
          color: AppColors.safeGreen,
        ),
      );
    }

    final map = FlutterMap(
      options: MapOptions(
        initialCenter: _center,
        initialZoom: 17,
        interactionOptions: InteractionOptions(
          flags: widget.interactive ? InteractiveFlag.all : InteractiveFlag.none,
        ),
      ),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'com.crisiscore.app',
        ),
        if (polylines.isNotEmpty) PolylineLayer(polylines: polylines),
        if (markers.isNotEmpty) MarkerLayer(markers: markers),
      ],
    );

    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: map,
    );
  }
}

class _StaffDot extends StatelessWidget {
  const _StaffDot();

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.primary,
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 2),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.3),
            blurRadius: 8,
            spreadRadius: 2,
          ),
        ],
      ),
    );
  }
}
