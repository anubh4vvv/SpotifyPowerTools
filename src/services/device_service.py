def get_available_devices(sp):
    """
    Returns available Spotify Connect devices.
    """

    response = sp.devices()

    devices = response.get(
        "devices",
        []
    )

    cleaned_devices = []

    for device in devices:

        cleaned_devices.append({
            "id": device.get("id", ""),
            "name": device.get("name", "Unknown Device"),
            "type": device.get("type", "Unknown"),
            "is_active": device.get("is_active", False),
            "is_restricted": device.get("is_restricted", False),
            "volume_percent": device.get("volume_percent"),
        })

    return cleaned_devices


def transfer_playback(sp, device_id):
    """
    Transfers Spotify playback to the selected device.
    """

    if not device_id:
        raise RuntimeError(
            "No device selected."
        )

    sp.transfer_playback(
        device_id=device_id,
        force_play=True
    )

    return {
        "device_id": device_id,
        "message": "Playback transferred"
    }