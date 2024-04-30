from substrateinterface import SubstrateInterface
from collections import OrderedDict
import json


class HydraDX:
    def __init__(self, url="wss://hydradx-rpc.dwellir.com"):
        self.substrate = SubstrateInterface(url=url, auto_reconnect=True, ws_options={'close_timeout': 15, 'open_timeout': 15})

    def system_accounts(self):
        print(f"Gathering all system accounts that hold HDX... please wait")
        data = {}
        result = self.substrate.query_map(module='System', storage_function='Account')
        for address, balances in result:
            total_balance = balances['data']['free'].value + balances['data']['reserved'].value
            data.update({address.value: total_balance})
        print(f"Complete!")
        return data

    def tokens_accounts(self):
        print(f"Gathering all accounts that hold assets on HDX... please wait")
        result = self.substrate.query_map(module='Tokens', storage_function='Accounts', params=[])
        print(f"Complete!")
        return result

    def asset_snapshot(self, token_data, asset_id: int):
        data = {}

        # system asset
        if asset_id == 0:
            data = self.system_accounts()
        else:
            for holder, balances in token_data:
                # holder: (<scale_info::0(value=7LgGj64Q5TA3NU5k99heKMAgpFTv5cMbnbqp7YdEeyabVqQU)>, <U32(value=5)>)
                # balances: {'free': 80730000000000000000, 'reserved': 0, 'frozen': 0}

                if holder[1].value == asset_id:
                    total_balance = balances['free'].value + balances['reserved'].value
                    data.update({holder[0].value: total_balance})

        with open(f'./data/assets_held/snapshot-asset-{asset_id}.json', 'w') as snapshot_output:
            sorted_data = OrderedDict(sorted(data.items(), key=lambda item: item[1], reverse=True))
            json.dump(sorted_data, snapshot_output, indent=4)

        print(f"Asset ID: {asset_id} - Holder(s): {len(data)}")
        return True

    def asset_registry_list(self):
        result = self.substrate.query_map(module='AssetRegistry', storage_function='Assets', params=[])
        asset_ids = []
        for asset_id, xcm_location in result:
            asset_ids.append(asset_id.value)

        asset_ids.sort()
        return asset_ids


if __name__ == '__main__':
    hdx = HydraDX()
    # snapshot of a single asset
    # hdx.asset_snapshot(asset_id=0)
    # hdx.asset_snapshot(asset_id=5)

    # snapshot all assets
    tokens_accounts = hdx.tokens_accounts()

    for uid in hdx.asset_registry_list():
        hdx.asset_snapshot(token_data=tokens_accounts, asset_id=uid)
