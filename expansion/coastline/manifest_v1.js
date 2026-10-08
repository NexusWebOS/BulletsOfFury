window.COAST_MANIFEST={"version":1,"project":"Bullets of Fury — Overdrive","region":"Miami coast","status":"Generated art candidates, not integrated gameplay","mapLayout":{"canvas":[2560,1280],"coast":{"rect":[70,45,780,1040]},"originalCampaign":{"origin":[1580,230],"scale":0.96,"positionSource":"Current game SSEL_POS / CM2_K 1.45 / offset 10"},"nodes":{"od01":[604,850],"od02":[505,665]},"direction":"Existing islands on right → long water crossing left → compound → north gate and highway"},"assets":[{"file":"assets/miami_coast_region.png","role":"Transparent campaign region","source":"source/miami_coast_region.png","width":768,"height":1024,"transparentPixels":229576,"partialAlphaPixels":556719,"sha256":"62c8e797b305521d8c5d23f8c0945c14b7e93931261e925fdf29a8c7ba6c87aa"},{"file":"assets/level_01_compound.png","role":"Campaign level icon; 190 logical pixels at 2x","source":"source/level_01_compound.png","width":380,"height":380,"transparentPixels":83020,"partialAlphaPixels":61353,"sha256":"5457b21757cf281f04a8b5c07d0903110e6049a94421e68fc82d8a60932f945c"},{"file":"assets/level_01_compound_128.png","role":"Thumbnail","source":"source/level_01_compound.png","width":128,"height":128,"transparentPixels":11156,"partialAlphaPixels":5228,"sha256":"d889ad49f8d79925dccf702ddc18c1d08f610d8c8e91ae1cfc2b0a43ca8a98e6"},{"file":"assets/level_02_gate_highway.png","role":"Campaign level icon; 190 logical pixels at 2x","source":"source/level_02_gate_highway.png","width":380,"height":380,"transparentPixels":63649,"partialAlphaPixels":80729,"sha256":"222f074e77246f6dc186080bbdac0938499a4194f9ec136166bc451b94599f0f"},{"file":"assets/level_02_gate_highway_128.png","role":"Thumbnail","source":"source/level_02_gate_highway.png","width":128,"height":128,"transparentPixels":9505,"partialAlphaPixels":6879,"sha256":"25dde5f4d43564684cbd9328c27fd95aa3fbf3691712712e504c94c54a1d7abe"},{"file":"assets/level_01_ocean_approach.png","role":"Finite transition background candidate; not seamless","source":"source/level_01_ocean_approach.png","width":480,"height":720,"transparentPixels":0,"partialAlphaPixels":0,"sha256":"cdc45ffd895e55323200f8e999c6f2f91d128dcd9e6aa6f3fb7b4e93bcc9d793"},{"file":"assets/level_02_coastal_highway.png","role":"Finite transition background candidate; not seamless","source":"source/level_02_coastal_highway.png","width":480,"height":720,"transparentPixels":0,"partialAlphaPixels":0,"sha256":"686c82df444613acf263c6d706f83f25fa3484eb4dcaa4114e93e2fde0377ae8"},{"file":"assets/connecting_map_clean.png","role":"Campaign layout composite; labels and routes separate","source":"Existing campaign island references + new coast region","width":2560,"height":1280,"transparentPixels":0,"partialAlphaPixels":0,"sha256":"9f6fca36be1ceb2fe7d0410f15ea8d5de93b0e6e734fc398bbe8f9ebb75b07e0"},{"file":"assets/connecting_map_route.png","role":"Review composite with proposed route and two mission markers","source":"connecting_map_clean.png + connecting_route.svg","width":2560,"height":1280,"transparentPixels":0,"partialAlphaPixels":0,"sha256":"dcc4980e2c96cebca8c0123bc8919aa5bf6957d73c8407dc61a9b31c03c6100e"}]};
window.COAST_STORY={
  "expansion": "Bullets of Fury — Overdrive",
  "region": "Miami coast, Florida",
  "status": "Art package and mission outline. No gameplay or campaign progression integration.",
  "canon": {
    "hotwireAndPhoenix": "Independent fighters pursuing their own cause, caught in the wider conflict. They hold an abandoned military compound together and help the player bring tanks online.",
    "enemyContext": "The symbiote has spread globally across Earth. Symbiotic alien ships attack on the ocean approach.",
    "shipStatus": "The player's ship is shot down into the compound just before entry. The player survives because Hotwire and Phoenix rescue them. The ship is temporarily unavailable while they attempt repairs.",
    "transition": "The rescued pilot receives a tank and leaves through the base's north gate, follows the coast, and heads inland toward Miami.",
    "laterContinuity": "The later tank-destruction / on-foot infiltration / jet-recovery mission is a separate event. Do not merge it into this arrival mission."
  },
  "missions": [
    {
      "id": "od01",
      "number": 1,
      "title": "Coastal Lifeline",
      "titleStatus": "Working title",
      "mode": "Flight → scripted rescue",
      "location": "Atlantic approach / abandoned military compound",
      "objective": "Cross the water and reach the military compound.",
      "icon": "assets/level_01_compound.png",
      "plate": "assets/level_01_ocean_approach.png",
      "beats": [
        "Fly far left/west from the existing campaign across open Atlantic water.",
        "Symbiotic alien ships ambush the player before the coastline.",
        "Hotwire and Phoenix make radio contact, welcome the arrival, and open the way inside.",
        "Immediately before entry, a hostile shot downs the player's ship into the base.",
        "Hotwire and Phoenix rescue the pilot and recover the damaged aircraft.",
        "They attempt ship repairs and bring the pilot's assigned tank online."
      ],
      "dialogueDraft": [
        {
          "speaker": "Hotwire",
          "line": "Phoenix, that's a pilot out there! Thank God someone showed up. Bring them in!"
        },
        {
          "speaker": "Phoenix",
          "line": "We've got the gate. Head for the hangar—we'll cover you."
        },
        {
          "speaker": "Hotwire",
          "line": "Incoming! Break—"
        },
        {
          "event": "The ship is hit before entry and crashes into the compound. Both allies rescue the pilot."
        },
        {
          "speaker": "Phoenix",
          "line": "Easy. We got you. You're inside the base."
        },
        {
          "speaker": "Hotwire",
          "line": "Your ship's in rough shape. We'll see what we can fix. Until then, let's get you a tank."
        }
      ]
    },
    {
      "id": "od02",
      "number": 2,
      "title": "Coast Under Siege",
      "titleStatus": "Working title",
      "mode": "Tank • air and ground threats",
      "location": "North gate / coastal highway / Miami approach",
      "objective": "Leave the compound, push up the coast, and reach the road inland toward Miami.",
      "icon": "assets/level_02_gate_highway.png",
      "plate": "assets/level_02_coastal_highway.png",
      "beats": [
        "The tank rolls out through the open military exit gate.",
        "Palm trees, beaches, sand, ocean and Miami architecture establish the new region.",
        "Ground units attack on the road and from its margins.",
        "Air units attack across the coast while the player remains in a ground tank.",
        "The road continues north along the water and turns inland toward Miami."
      ],
      "dialogueDraft": [
        {
          "speaker": "Hotwire",
          "line": "Tank's online. Take the north gate and stay on the coast road."
        },
        {
          "speaker": "Phoenix",
          "line": "That highway leads into Miami. Keep watching the sky—they're hitting the ground too."
        }
      ]
    }
  ],
  "productionNotes": [
    "Mission names and dialogue are drafts; the user's story beats above are the canon.",
    "Do not depict Hotwire or Phoenix as rogue or rebel faction members.",
    "Arrival crash is a story transition, not a normal death/game-over. Exact implementation remains future work.",
    "Campaign route endpoint at the old island cluster is a layout proposal; its unlock trigger and exact existing stage attachment are not chosen here.",
    "This map represents game geography, not a navigational map of real Miami.",
    "The two background plates are finite illustrated transition sections, not seamless tiles, collision maps or complete scrolling levels.",
    "The arrival source includes a small decorative tank in the side service bay and fixed defense guns. Treat them as scenery unless extracted and replaced during production.",
    "The highway source has a narrow central carriageway. Future playable stage assembly must add wide road/shoulder tiles for bullet-dodging space; do not infer collision bounds from the image."
  ]
}
;
