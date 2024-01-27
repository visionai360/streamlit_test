import streamlit as st
import rasterio

def read_tif(tif_path):
    with rasterio.open(tif_path) as dataset:
        width = dataset.width
        height = dataset.height
        num_bands = dataset.count
        crs = dataset.crs

        raster = dataset.read()

    return width, height, num_bands, crs, raster

def main():
    st.title("TIF File Reader")
    
    # Create a file upload dialog
    uploaded_file = st.file_uploader("Upload a TIF file", type=["tif", "tiff"])

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the contents of the file
        tif_contents = uploaded_file.read()

        # Open the TIF file using rasterio
        with rasterio.MemoryFile(tif_contents) as memfile:
            with memfile.open() as dataset:
                width = dataset.width
                height = dataset.height
                num_bands = dataset.count
                crs = dataset.crs

                meta = dataset.meta
                raster_org = dataset.read()
        
        raster = raster_org[0]
        m = raster.max() + 1
        raster[0:2,:] = m
        raster[-2:,:] = m
        raster[:,0:2] = m
        raster[:,-2:] = m

        no_data_mask = raster==-32767
        raster[no_data_mask] = m


        # Display the file properties
        st.write("Width:", width)
        st.write("Height:", height)
        st.write("Number of bands:", num_bands)
        st.write("CRS:", crs)
        st.write("Raster shape:", raster.shape)

if __name__ == "__main__":
    main()
