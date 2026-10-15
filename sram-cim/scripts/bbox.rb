ly = RBA::Layout.new
ly.read(File.expand_path("~/designs/mac8/libraries/sram_6t/SRAMCIMsbc/SRAMCIMsbc.gds"))
c = ly.cell("SRAMCIMsbc")
b = c.dbbox
pr = ly.find_layer(RBA::LayerInfo.new(100,0)) rescue nil
puts "bbox #{b.left} #{b.bottom} #{b.right} #{b.top} w=#{b.width.round(4)} h=#{b.height.round(4)} cpp=#{(b.width/0.054).round(2)}"
