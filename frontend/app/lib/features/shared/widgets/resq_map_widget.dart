import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

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

  String? _mapStyle;
  late Set<Marker> _markers;
  late Set<Polyline> _polylines;

  @override
  void initState() {
    super.initState();
    _markers = _buildMarkers();
    _polylines = _buildPolylines();
    _loadMapStyle();
  }

  @override
  void didUpdateWidget(covariant ResQMapWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.showIncidentPin != widget.showIncidentPin ||
        oldWidget.showStaffDots != widget.showStaffDots ||
        oldWidget.showEvacRoute != widget.showEvacRoute) {
      setState(() {
        _markers = _buildMarkers();
        _polylines = _buildPolylines();
      });
    }
  }

  Future<void> _loadMapStyle() async {
    final style = await rootBundle.loadString('assets/map_style_dark.json');
    if (!mounted) {
      return;
    }

    setState(() {
      _mapStyle = style;
    });
  }

  Set<Marker> _buildMarkers() {
    final markers = <Marker>{};

    if (widget.showIncidentPin) {
      markers.add(
        Marker(
          markerId: const MarkerId('incident'),
          position: const LatLng(19.0767, 72.8780),
          icon: BitmapDescriptor.defaultMarkerWithHue(
            BitmapDescriptor.hueRed,
          ),
          infoWindow: const InfoWindow(title: 'Active Incident'),
        ),
      );
    }

    if (widget.showStaffDots) {
      markers.addAll(
        [
          Marker(
            markerId: const MarkerId('staff_1'),
            position: const LatLng(19.0758, 72.8769),
            icon: BitmapDescriptor.defaultMarkerWithHue(
              BitmapDescriptor.hueAzure,
            ),
          ),
          Marker(
            markerId: const MarkerId('staff_2'),
            position: const LatLng(19.0762, 72.8775),
            icon: BitmapDescriptor.defaultMarkerWithHue(
              BitmapDescriptor.hueAzure,
            ),
          ),
          Marker(
            markerId: const MarkerId('staff_3'),
            position: const LatLng(19.0764, 72.8786),
            icon: BitmapDescriptor.defaultMarkerWithHue(
              BitmapDescriptor.hueAzure,
            ),
          ),
        ],
      );
    }

    return markers;
  }

  Set<Polyline> _buildPolylines() {
    if (!widget.showEvacRoute) {
      return const <Polyline>{};
    }

    return {
      const Polyline(
        polylineId: PolylineId('evac_route'),
        color: AppColors.safeGreen,
        width: 5,
        points: [
          LatLng(19.0757, 72.8768),
          LatLng(19.0761, 72.8774),
          LatLng(19.0764, 72.8779),
          LatLng(19.0768, 72.8785),
        ],
      ),
    };
  }

  @override
  Widget build(BuildContext context) {
    final map = GoogleMap(
      initialCameraPosition: const CameraPosition(
        target: _center,
        zoom: 17,
      ),
      myLocationEnabled: false,
      myLocationButtonEnabled: false,
      mapToolbarEnabled: false,
      zoomControlsEnabled: false,
      compassEnabled: false,
      style: _mapStyle,
      markers: _markers,
      polylines: _polylines,
    );

    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: widget.interactive ? map : AbsorbPointer(child: map),
    );
  }
}
