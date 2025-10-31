import sys
sys.path.append('/Users/mike/Documents/adapter_training_toolkit_v26_0_0')

from export.produce_asset_pack import AssetPackBuilder, produce_asset_pack

produce_asset_pack(
    fmadapter_path='trained_adapter/uebersicht_widgets_fmadapter',
    output_path='trained_adapter/uebersicht_widgets.aar',
    platforms=[AssetPackBuilder.Platforms.iOS, AssetPackBuilder.Platforms.macOS],
    download_policy=AssetPackBuilder.DownloadPolicy.PREFETCH,   # type: ignore
    installation_event_type=AssetPackBuilder.InstallationEventType.FIRST_INSTALLTION   # type: ignore
)
