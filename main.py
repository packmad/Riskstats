from asset_manager import AssetsManager


if __name__ == '__main__':
    AM = AssetsManager()
    for asset in AM.assets:
        print(asset)
