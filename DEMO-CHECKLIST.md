# Khoj Doot - Demo Checklist

## 1. Shop Seed Data

- [ ] 10 shops are included in `seed-data/shops.json`
- [ ] Every shop has a unique `sme_id`
- [ ] Every shop has a unique `slug`
- [ ] Shop name is present
- [ ] Category is present
- [ ] City and state are present
- [ ] Phone number is included where available
- [ ] Address is included
- [ ] Product/offerings information is included
- [ ] Rate information is included where known
- [ ] No invented prices are added
- [ ] `does_not_do` is included for shop constraints
- [ ] Date and source fields are included

## 2. Photos

- [ ] 40 shop photos are available
- [ ] Photos are stored inside the `image` folder
- [ ] Photos are associated with the correct SME
- [ ] Photo filenames match the filenames stored in `shops.json`

## 3. Shop Identity

- [ ] Each shop has a unique public slug
- [ ] Shop information can be represented as structured shop memory
- [ ] Product information is separated from shop identity
- [ ] Price information is separated from product information
- [ ] Missing information is not invented

## 4. Public Shop Page Demo

- [ ] Open the public shop page using the shop slug
- [ ] Shop name is visible
- [ ] Category is visible
- [ ] Location is visible
- [ ] Contact information is visible where available
- [ ] Products/services are visible
- [ ] Rates are visible when available
- [ ] "Rates on request" is shown when applicable
- [ ] Shop constraints are visible when applicable
- [ ] Photos are visible

## 5. Trust Checks

- [ ] Shop information is discrete and structured
- [ ] Source/date information is available
- [ ] No price is invented when it is unknown
- [ ] No live stock is claimed from photos
- [ ] Missing information is handled safely
- [ ] Shop claims can be traced back to the seed data

## 6. Demo Flow

1. Select a shop from the seed data.
2. Open its public shop page.
3. Verify the shop name and location.
4. Check the available products/services.
5. Check the available rate information.
6. Check the shop photos.
7. Check any constraints or additional reliable facts.
8. Verify that no unsupported information is displayed.

## 7. Prototype Scope

The prototype does NOT require:

- [ ] Login system
- [ ] Payment system
- [ ] Checkout
- [ ] E-commerce ordering
- [ ] ONDC seller node
- [ ] Live inventory from photos
- [ ] Invented prices