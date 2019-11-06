%Code Description: takes RGB color inputs from folder and creates greyscale
%image with blue dye color only emphasized
%Author: Teresa Jarriel
%Department of Environmental and Water Resources Engineering, UT Austin
%Email: teresa.jarriel@utexas.edu
%Created: 3/12/2018
%Last Revision: 4/10/2018


%input your path to folder containing images to analyze here
path_test='E:\SIESD 2017\ImagesByCycle\Cycle6_images\RGB_images';
file_test=fullfile(path_test,'*.jpg');
d=dir(file_test);
for k=1:numel(d)
    %---------------------------read in image-----------------------------
    filename=fullfile(path_test,d(k).name);
    I=imread(filename);
    %optional visualization
    figure,imshow(I)
    title('Original Color Image');
    YCbCr=rgb2ycbcr(I);
    %----------------------separate into three bands----------------------
    Image_Cr= YCbCr(:, :, 3);
%    figure, imshow(Image_Cr,[])
    Image_Cr_comp=imcomplement(Image_Cr);
    Final=imadjust(Image_Cr_comp, [.27 .7],[.49 1],4);
    figure, imshow(Final);
    Final2=imadjust(Final);
    figure, imshow(Final2)
    
%     figure, imshow(Image_Cr_comp,[])
%     figure, imshow(Final)
    finalUINT8=im2uint8(Image_Cr_comp);
%    imwrite(finalUINT8,strcat(filename,'_RGBtoYCbCr','.TIF'))

end
