/**
 * International Trademark Classes (Nice Classification)
 * Classes 1-34: Goods
 * Classes 35-45: Services
 */

export interface TrademarkClass {
  number: string
  type: 'goods' | 'services'
  description: string
}

export const TRADEMARK_CLASSES: TrademarkClass[] = [
  // GOODS (Classes 1-34)
  { number: '001', type: 'goods', description: 'Chemicals, adhesives, fire extinguishing compositions' },
  { number: '002', type: 'goods', description: 'Paints, varnishes, lacquers, preservatives against rust' },
  { number: '003', type: 'goods', description: 'Cosmetics, cleaning preparations, essential oils' },
  { number: '004', type: 'goods', description: 'Industrial oils and greases, lubricants, fuels, candles' },
  { number: '005', type: 'goods', description: 'Pharmaceuticals, medical supplies, dietary supplements' },
  { number: '006', type: 'goods', description: 'Common metals and their alloys, metal building materials' },
  { number: '007', type: 'goods', description: 'Machines and machine tools, motors and engines' },
  { number: '008', type: 'goods', description: 'Hand tools and implements, cutlery, razors' },
  { number: '009', type: 'goods', description: 'Scientific apparatus, computers, software, electronics' },
  { number: '010', type: 'goods', description: 'Surgical and medical apparatus and instruments' },
  { number: '011', type: 'goods', description: 'Lighting, heating, cooking, refrigerating apparatus' },
  { number: '012', type: 'goods', description: 'Vehicles, apparatus for locomotion by land, air or water' },
  { number: '013', type: 'goods', description: 'Firearms, ammunition, explosives, fireworks' },
  { number: '014', type: 'goods', description: 'Precious metals, jewelry, timepieces and chronometric instruments' },
  { number: '015', type: 'goods', description: 'Musical instruments' },
  { number: '016', type: 'goods', description: 'Paper, cardboard, printed matter, stationery, office supplies' },
  { number: '017', type: 'goods', description: 'Rubber, gutta-percha, insulating materials, flexible pipes' },
  { number: '018', type: 'goods', description: 'Leather and imitations, animal skins, luggage, bags' },
  { number: '019', type: 'goods', description: 'Non-metallic building materials' },
  { number: '020', type: 'goods', description: 'Furniture, mirrors, picture frames, containers' },
  { number: '021', type: 'goods', description: 'Household utensils, cookware, glassware, porcelain' },
  { number: '022', type: 'goods', description: 'Ropes, string, nets, tents, awnings, sails, bags' },
  { number: '023', type: 'goods', description: 'Yarns and threads for textile use' },
  { number: '024', type: 'goods', description: 'Textiles and textile goods, bed covers, table covers' },
  { number: '025', type: 'goods', description: 'Clothing, footwear, headgear' },
  { number: '026', type: 'goods', description: 'Lace, embroidery, ribbons, buttons, pins and needles' },
  { number: '027', type: 'goods', description: 'Carpets, rugs, mats, linoleum, wall hangings' },
  { number: '028', type: 'goods', description: 'Games, toys, sporting articles, decorations for Christmas trees' },
  { number: '029', type: 'goods', description: 'Meat, fish, poultry, preserved/frozen/dried fruits and vegetables' },
  { number: '030', type: 'goods', description: 'Coffee, tea, cocoa, sugar, rice, flour, bread, pastry, confectionery' },
  { number: '031', type: 'goods', description: 'Agricultural products, fresh fruits and vegetables, live animals' },
  { number: '032', type: 'goods', description: 'Beers, mineral waters, soft drinks, fruit juices' },
  { number: '033', type: 'goods', description: 'Alcoholic beverages (except beers)' },
  { number: '034', type: 'goods', description: 'Tobacco, smokers\' articles, matches' },

  // SERVICES (Classes 35-45)
  { number: '035', type: 'services', description: 'Advertising, business management, office functions, retail services' },
  { number: '036', type: 'services', description: 'Insurance, financial affairs, monetary affairs, real estate' },
  { number: '037', type: 'services', description: 'Building construction, repair, installation services' },
  { number: '038', type: 'services', description: 'Telecommunications' },
  { number: '039', type: 'services', description: 'Transport, packaging and storage of goods, travel arrangement' },
  { number: '040', type: 'services', description: 'Treatment of materials, custom manufacturing' },
  { number: '041', type: 'services', description: 'Education, training, entertainment, sporting and cultural activities' },
  { number: '042', type: 'services', description: 'Scientific and technological services, software development, design' },
  { number: '043', type: 'services', description: 'Food and drink services, temporary accommodation' },
  { number: '044', type: 'services', description: 'Medical services, veterinary services, beauty and agriculture' },
  { number: '045', type: 'services', description: 'Legal services, security services, personal and social services' },
]

export const getClassesByType = (type: 'goods' | 'services' | 'all' = 'all') => {
  if (type === 'all') return TRADEMARK_CLASSES
  return TRADEMARK_CLASSES.filter(c => c.type === type)
}

export const getClassByNumber = (number: string) => {
  return TRADEMARK_CLASSES.find(c => c.number === number)
}
