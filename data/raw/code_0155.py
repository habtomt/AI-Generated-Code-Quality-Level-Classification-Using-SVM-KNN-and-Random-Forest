import hashlib

class NFT:
    def __init__(self, token_id, metadata, owner):
        self.token_id = token_id
        self.metadata = metadata
        self.owner = owner
        self.history = [owner]

class NFTMarketplace:
    def __init__(self):
        self.nfts = {}
        self.token_counter = 1

    def mint_nft(self, creator, metadata):
        token_id = hashlib.sha1(str(self.token_counter).encode()).hexdigest()[:8]
        new_nft = NFT(token_id, metadata, creator)
        self.nfts[token_id] = new_nft
        self.token_counter += 1
        print(f"Minted: {metadata} with ID {token_id} for {creator}")
        return token_id

    def transfer_nft(self, token_id, current_owner, new_owner):
        if token_id in self.nfts and self.nfts[token_id].owner == current_owner:
            self.nfts[token_id].owner = new_owner
            self.nfts[token_id].history.append(new_owner)
            print(f"Transferred: {token_id} from {current_owner} to {new_owner}")
        else:
            print("Transfer Failed: Unauthorized or Invalid Token")

# Execution
market = NFTMarketplace()
art_id = market.mint_nft("Artist_X", "Digital Portrait #01")
market.transfer_nft(art_id, "Artist_X", "Collector_Y")
print(f"Current Owner of {art_id}: {market.nfts[art_id].owner}")