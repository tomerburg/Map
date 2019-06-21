import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
from mpl_toolkits.axes_grid1 import make_axes_locatable

import cartopy
import cartopy.feature as cfeature
from cartopy import crs as ccrs
from cartopy import util as cu

from metpy.plots import USCOUNTIES

#================================================================================================

class Map():
    
    def __init__(self,projection='PlateCarree',ax=None,res='m',**kwargs):
        """
        Initialize a Map instance with a passed Cartopy projection which this object acts
        as a wrapper for.
        
        Parameters:
        ----------------------
        projection
            String representing the cartopy map projection.
        ax
            Axis on which to draw on. Default is None.
        res
            String representing the default geography boundary resolution ('l'=low,'m'=moderate,'h'=high).
            Default resolution is moderate 'm'. This can also be changed individually for each function
            that plots boundaries.
        **kwargs
            Additional arguments that are passed to those associated with projection.
            
        Returns:
        ----------------------
        Instance of a Map object
        """
        
        self.proj = getattr(ccrs, projection)(**kwargs)
        self.ax = ax
        self.res = res
        
    def check_for_digits(self,text):
        """
        Checks if a string contains digits.
        
        Parameters:
        ----------------------
        text
            String to check for digits
            
        Returns:
        ----------------------
        Boolean, True if string contains digits, otherwise False
        """
        
        check = False
        for i in text:
            if i.isdigit(): check = True
        return check
        
    def check_res(self,res,counties=False):
        """
        Checks if a resolution string contains digits. If yes, then that value is returned
        and is passed into the cartopy "with_scale()" argument. If it's solely a string
        representing the type of resolution ('l','m','h'), then that value is converted to
        a resolution with digits depending on the type of boundary being plotted.
        
        Parameters:
        ----------------------
        res
            String representing the passed resolution
            
        Returns:
        ----------------------
        String representing the converted resolution
        """
        
        #If resolution contains digits (e.g., '50m'), assumed to be valid input and simply returned
        if self.check_for_digits(res) == True:
            return res
        
        #Otherwise, attach numerical values to low, medium and high resolutions
        else:
            #Use cartopy's available options for everything but counties
            if counties == False:
                if res == 'l':
                    return '110m'
                elif res == 'h':
                    return '10m'
                else:
                    return '50m'
            #Use MetPy's available options for county resolutions
            else:
                if res == 'l':
                    return '20m'
                elif res == 'h':
                    return '500k'
                else:
                    return '5m'
    
    def drawcoastlines(self,linewidths=1.2,linestyle='solid',color='k',res=None,ax=None,**kwargs):
        """
        Draws coastlines similarly to Basemap's m.drawcoastlines() function.
        
        Parameters:
        ----------------------
        linewidths
            Line width (default is 1.2)
        linestyle
            Line style to plot (default is solid)
        color
            Color of line (default is black)
        res
            Resolution of coastline. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Draw coastlines
        coastlines = ax.add_feature(cfeature.COASTLINE.with_scale(res),linewidths=linewidths,linestyle=linestyle,edgecolor=color,**kwargs)
        
        #Return value
        return coastlines
    
    def drawcountries(self,linewidths=1.2,linestyle='solid',color='k',res=None,ax=None,**kwargs):
        """
        Draws country borders similarly to Basemap's m.drawcountries() function.
        
        Parameters:
        ----------------------
        linewidths
            Line width (default is 1.2)
        linestyle
            Line style to plot (default is solid)
        color
            Color of line (default is black)
        res
            Resolution of country borders. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Draw coastlines
        countries = ax.add_feature(cfeature.BORDERS.with_scale(res),linewidths=linewidths,linestyle=linestyle,edgecolor=color,**kwargs)
        
        #Return value
        return countries
    
    def drawstates(self,linewidths=0.7,linestyle='solid',color='k',res=None,ax=None,**kwargs):
        """
        Draws state borders similarly to Basemap's m.drawstates() function.
        
        Parameters:
        ----------------------
        linewidths
            Line width (default is 0.7)
        linestyle
            Line style to plot (default is solid)
        color
            Color of line (default is black)
        res
            Resolution of state borders. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Draw coastlines
        states = ax.add_feature(cfeature.STATES.with_scale(res),linewidths=linewidths,linestyle=linestyle,edgecolor=color,**kwargs)
        
        #Return value
        return states
    
    def filloceans(self,color='#C8E7FF',res=None,ax=None,**kwargs):
        """
        Fills oceans with solid colors.
        
        Parameters:
        ----------------------
        color
            Fill color for oceans (default is light blue)
        res
            Resolution of data. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Fill oceans
        ocean_mask = ax.add_feature(cfeature.OCEAN.with_scale(res),facecolor=color,edgecolor='face',**kwargs)
        
    def filllakes(self,color='#C8E7FF',res=None,ax=None,**kwargs):
        """
        Fills lakes with solid colors.
        
        Parameters:
        ----------------------
        color
            Fill color for lakes (default is light blue)
        res
            Resolution of data. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Fill lakes
        lake_mask = ax.add_feature(cfeature.LAKES.with_scale(res),facecolor=color,edgecolor='face',**kwargs)
        
        #Return value
        return lake_mask
    
    def fillcontinents(self,color='#e6e6e6',res=None,ax=None,**kwargs):
        """
        Fills land with solid colors.
        
        Parameters:
        ----------------------
        color
            Fill color for land (default is light gray)
        res
            Resolution of data. Can be a character ('l','m','h') or one of cartopy's available
            resolutions ('110m','50m','10m'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        if res is None: res = self.res
        res = self.check_res(res)
        
        #Fill continents
        continent_mask = ax.add_feature(cfeature.LAND.with_scale(res),facecolor=color,edgecolor='face',**kwargs)
        
        #Return value
        return continent_mask
    
    def drawcounties(self,linewidths=0.2,linestyle='solid',color='k',res='l',ax=None,**kwargs):
        """
        Draws county borders similarly to Basemap's m.drawcounties() function. Since cartopy currently
        does not offer a county shapefile, this function uses MetPy's available county shapefiles.
        
        Parameters:
        ----------------------
        linewidths
            Line width (default is 0.2)
        linestyle
            Line style to plot (default is solid)
        color
            Color of line (default is black)
        res
            Resolution of country borders. Can be a character ('l','m','h') or one of MetPy's available
            resolutions ('20m','5m','500k'). If none is specified, then the default resolution specified
            when creating an instance of Map is used.
        ax
            Axes instance, if not None then overrides the default axes instance.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Error check resolution
        res = self.check_res(res,counties=True)
        
        #Draw counties using metpy
        counties = ax.add_feature(USCOUNTIES.with_scale(res),linewidths=linewidths,linestyle=linestyle,edgecolor=color,**kwargs)
        
        #Return value
        return counties
    
    def _check_ax(self):
        """
        Adapted from Basemap - checks to see if an axis is specified, if not, returns plt.gca().
        """
        
        if self.ax is None:
            try:
                ax = plt.gca(projection=self.proj)
            except:
                import matplotlib.pyplot as plt
                ax = plt.gca(projection=self.proj)
        else:
            ax = self.ax(projection=self.proj)
            
        return ax
        
    def colorbar(self,mappable=None,location='right',size="3%",pad='1%',fig=None,ax=None,**kwargs):
        """
        Uses the axes_grid toolkit to add a colorbar to the parent axis and rescale its size to match
        that of the parent axis, similarly to Basemap's functionality.
        
        Parameters:
        ----------------------
        mappable
            The image mappable to which the colorbar applies. If none specified, matplotlib.pyplot.gci() is
            used to retrieve the latest mappable.
        location
            Location in which to place the colorbar ('right','left','top','bottom'). Default is right.
        size
            Size of the colorbar. Default is 3%.
        pad
            Pad of colorbar from axis. Default is 1%.
        ax
            Axes instance to associated the colorbar with. If none provided, or if no
            axis is associated with the instance of Map, then plt.gca() is used.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Get current mappable if none is specified
        if fig is None or mappable is None:
            import matplotlib.pyplot as plt
        if fig is None:
            fig = plt.gcf()
            
        if mappable is None:
            mappable = plt.gci()
        
        #Create axis to insert colorbar in
        divider = make_axes_locatable(ax)
        
        if location == "left":
            orientation = 'vertical'
            ax_cb = divider.new_horizontal(size, pad, pack_start=True, axes_class=plt.Axes)
        elif location == "right":
            orientation = 'vertical'
            ax_cb = divider.new_horizontal(size, pad, pack_start=False, axes_class=plt.Axes)
        elif location == "bottom":
            orientation = 'horizontal'
            ax_cb = divider.new_vertical(size, pad, pack_start=True, axes_class=plt.Axes)
        elif location == "top":
            orientation = 'horizontal'
            ax_cb = divider.new_vertical(size, pad, pack_start=False, axes_class=plt.Axes)
        else:
            raise ValueError('Improper location entered')
        
        #Create colorbar
        fig.add_axes(ax_cb)
        cb = plt.colorbar(mappable, orientation=orientation, cax=ax_cb, **kwargs)
        
        #Reset parent axis as the current axis
        fig.sca(ax)
        return cb

    def contourf(self,lon,lat,data,*args,ax=None,transform=None,**kwargs):
        """
        Wrapper to matplotlib's contourf function. Assumes lat and lon arrays are passed instead
        of x and y arrays. Default data projection is ccrs.PlateCarree() unless a different
        data projection is passed.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Check transform if not specified
        if transform is None: transform = ccrs.PlateCarree()
        
        #Fill contour data
        cs = ax.contourf(lon,lat,data,*args,**kwargs,transform=transform)
        return cs
    
    def contour(self,lon,lat,data,*args,ax=None,transform=None,**kwargs):
        """
        Wrapper to matplotlib's contour function. Assumes lat and lon arrays are passed instead
        of x and y arrays. Default data projection is ccrs.PlateCarree() unless a different
        data projection is passed.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Check transform if not specified
        if transform is None: transform = ccrs.PlateCarree()
        
        #Contour data
        cs = ax.contour(lon,lat,data,*args,**kwargs,transform=transform)
        return cs
    
    def barbs(self,lon,lat,u,v,*args,ax=None,transform=None,**kwargs):
        """
        Wrapper to matplotlib's barbs function. Assumes lat and lon arrays are passed instead
        of x and y arrays. Default data projection is ccrs.PlateCarree() unless a different
        data projection is passed. Flips barbs for southern hemisphere.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Check transform if not specified
        if transform is None: transform = ccrs.PlateCarree()
        
        #Ensure lon and lat arrays are 2D
        lon_shape = len(np.array(lon).shape)
        lat_shape = len(np.array(lat).shape)
        if lon_shape == 1 and lat_shape == 1:
            lon,lat = np.meshgrid(lon,lat)
        elif lon_shape == 2 and lat_shape == 2:
            pass
        else:
            raise ValueError('Both lon and lat must have the same number of dimensions')
        
        #Plot north hemisphere barbs
        u_nh = u.copy(); u_nh[np.logical_or(lat < 0.0,lat == 90.0)] = np.nan
        v_nh = v.copy(); v_nh[np.logical_or(lat < 0.0,lat == 90.0)] = np.nan
        barb_nh = ax.barbs(lon,lat,u_nh,v_nh,*args,**kwargs,transform=transform)
        
        #Plot south hemisphere barbs
        u_sh = u.copy(); u_sh[np.logical_or(lat > 0.0,lat == -90.0)] = np.nan
        v_sh = v.copy(); v_sh[np.logical_or(lat > 0.0,lat == -90.0)] = np.nan
        kwargs['flip_barb'] = True
        barb_sh = ax.barbs(lon,lat,u_sh,v_sh,*args,**kwargs,transform=transform)
        
        #Return values
        return barb_nh, barb_sh
    
    def quiver(self,lon,lat,u,v,*args,ax=None,transform=None,**kwargs):
        """
        Wrapper to matplotlib's quiver function. Assumes lat and lon arrays are passed instead
        of x and y arrays. Default data projection is ccrs.PlateCarree() unless a different
        data projection is passed.
        """
        
        #Get current axes if not specified
        ax = ax or self._check_ax()
        
        #Check transform if not specified
        if transform is None: transform = ccrs.PlateCarree()

        #Plot north hemisphere barbs
        qv = ax.quiver(lon,lat,u,v,*args,**kwargs,transform=transform)

        #Return values
        return qv
