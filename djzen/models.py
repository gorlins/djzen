"""Model definitions for Djzen"""
"""
    Copyright 2009 Scott Gorlin

    This file is part of Djzen.

    Djzen is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Djzen is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Djzen.  If not, see <http://www.gnu.org/licenses/>.
"""
from django.db import models
import zenapi
from django.core.urlresolvers import reverse
#from django.db.models import Q

#from django.utils.safestring import mark_safe
# Create your models here.

setByZen = dict(editable=False, null=True, blank=True)

# Helper class
class Enum(object):
    def __init__(self, **kwargs):
        self.__dict = {}
        for k,v in kwargs.items():
            self.__dict[k]=v
            setattr(self, k, v)
            
    def __call__(self, typename):
        return self.__dict[typename]
    
    #def _getter(self, attr):
        #def get(self):
            #return self.__dict[attr]
        #return property(instancemethod(get))
    @property
    def choices(self):
        l = []
        for k,v in self.__dict.items():
            l.append((v, k))
        return tuple(l)
    
# Models
class ZenModel(models.Model):
    class Meta:
        abstract=True
        
    def _sync(self, synckwds, obj):
        
        for k in synckwds:
            if '_' in k:
                continue
            v = getattr(obj, k, None)
            if isinstance(v, zenapi._zapi.DateTime):
                v = v.Value
            if v is not None:
                setattr(self, k, v)
        self.save()
        
class User(ZenModel):
    """Model the Zenfolio user from which to snag photos"""
    #_id = models.IntegerField(primary_key=True, db_index=True)
    
    LoginName = models.CharField(max_length=60, db_index=True,
                                 unique=True, blank=False, null=False)
    DisplayName = models.CharField(max_length=60, **setByZen)
    
    # These are unfortunately private
    #FirstName = models.CharField(max_length=60, **setByZen)
    #LastName = models.CharField(max_length=60, **setByZen)    
    #PrimaryEmail = models.EmailField(**setByZen)
    
    Bio = models.TextField(**setByZen)
    Views = models.IntegerField(**setByZen)
    GalleryCount = models.IntegerField(**setByZen)
    CollectionCount = models.IntegerField(**setByZen)
    PhotoCount = models.IntegerField(**setByZen)
    PhotoBytes = models.IntegerField(**setByZen)
    UserSince = models.DateTimeField(**setByZen)
    LastUpdated = models.DateTimeField(**setByZen)
    
    #This is a dict and isn't yet handled properly
    #PublicAddress = models.CharField(max_length=100, **setByZen)
    
    # Relational mapping to external DB doesn't work so well, so we
    # go off Id's here and in other places
    #RecentPhotoSets = models.ManyToManyField('PhotoSet') #not right
    #FeaturedPhotoSets = models.ManyToManyField('PhotoSet')
    
    RootGroup = models.ForeignKey('Group', **setByZen)
    #RootGroup = models.IntegerField(**setByZen) # Id of root group
    
    DomainName = models.CharField(max_length=100, **setByZen)
    """
    User
    { + = public
        #+string LoginName,
        #+string DisplayName,
        string FirstName,
        string LastName,
        string PrimaryEmail,
        +File BioPhoto,
        #+string Bio,
        #+int Views,
        #+int GalleryCount,
        #+int CollectionCount,
        #+int PhotoCount,
        #+long PhotoBytes,
        #+DateTime UserSince,
        #+DateTime LastUpdated,
        #+Address PublicAddress,
        Address PersonalAddress,
        #+PhotoSet[] RecentPhotoSets,
        #+PhotoSet[] FeaturedPhotoSets,
        #+Group RootGroup,
        string ReferralCode,
        DateTime ExpiresOn,
        decimal Balance,
        #+string DomainName,
        long StorageQuota,
        long PhotoBytesQuota
    }
    """
    def __unicode__(self):
        return self.LoginName
    
    def update(self, updateChildren=False):
        zc = self.getConnection()
        ro = zc.LoadPublicProfile()
        synckeys = self.__dict__.keys()
        #synckeys.remove('RootGroup_id')
        
        self._sync(synckeys, ro)
        
        try:
            self.RootGroup = Group.objects.get(Id=ro.RootGroup.Id)
        except Group.DoesNotExist:
            self.RootGroup = Group(Id=ro.RootGroup.Id, Owner=self)
        if updateChildren:
            self.RootGroup.update(groupResponse=zc.loadFullGroupHierarchy(),
                                  updateChildren=updateChildren,
                                  fullyLoaded=True)
        self.save()
        
    def getConnection(self):
        return zenapi.ZenConnection(username=self.LoginName)
    
class GalleryElement(ZenModel):
    """Abstract base for all photos, photosets, and groups
    
    Note that the API doesn't contain this object, but the hierarchy's better
    this way
    """
    Id = models.IntegerField(primary_key=True, db_index=True, **setByZen)
    Title = models.CharField(max_length=100, **setByZen)
    #AccessDescriptor
    Caption = models.CharField(max_length=100, **setByZen)
    PageUrl = models.URLField(**setByZen)
    
    class Meta:
        abstract=True
        
    def get_absolute_url(self):
        return reverse('djzen-'+self.__class__.__name__.lower(), kwargs={'object_id':self.Id})
            
    def __unicode__(self):
        t = self.Title
        if not t:
            t = self.Caption
        if not t:
            t = self.__class__.__name__
        return t
    
    def zenlink(self):
        return '<a href="%s">%s</a>'%(self.PageUrl, self.PageUrl)
    zenlink.allow_tags=True
    
    def zenthumb(self):
        return 
    @property
    def titlelink(self):
        return '<a href="%s">%s</a>'%(self.PageUrl, self.Title)
    #titlelink.allow_tags=True
    
class GroupElement(GalleryElement):
    """Abstract base for photosets and groups"""
    GroupIndex = models.IntegerField(**setByZen)
    TitlePhoto = models.ForeignKey('Photo', **setByZen) 
    CreatedOn = models.DateTimeField(**setByZen)#switch from api
    ModifiedOn = models.DateTimeField(**setByZen)
    # Not accessable through API
    #CustomReference = models.CharField(max_length=100, **setByZen) 
    
    """
    GroupElement
    {
        int GroupIndex,
        string Title,
        AccessDescriptor AccessDescriptor,
        string Owner
    }
    """
    class Meta:
        abstract = True
        ordering = ['Title', 'Id']
    
    def ancestry(self):
        if self.ParentGroups.all():
            # Haven't yet solved multiple inheritance
            parent = self.ParentGroups.all()[0]
            return parent.ancestry() + [parent]
        return []
        
class Group(GroupElement):
    """Folder-like collection of groups and photosets"""
    
    #ParentGroups = models.ManyToManyField('self', related_name='GroupElements',
                                          #symmetrical=False) # in GroupElements
                                          
                                          
    Owner = models.ForeignKey(User, **setByZen)
    # Break API (from Elements) since we can't mix two classes in relations
    GroupElements = models.ManyToManyField('self', symmetrical=False,
                                           related_name='ParentGroups',
                                           **setByZen)
    PhotoSetElements = models.ManyToManyField('PhotoSet',
                                              related_name='ParentGroups', 
                                              **setByZen)
    # better separation this way anyways ;)
    
    """If this Group object only contains a single PhotoSet with the same title
    (and contains no child groups), the UI will try to flatten the tree 
    structure by replacing this group with the photoset where (i.e., the
    photoset will be listed in the parent's children instead of this group.  If 
    these conditions are met this value is autoset to True during calls to 
    self.update(), and setting back to False will prevent such behavior."""
    FlattenMe = models.BooleanField(default=False, editable=True,
                                  help_text="If True, the child PhotoSet will"+\
                                  " be extracted")
    
    """
    Group : GroupElement
    {
        #string Caption,
        #DateTime CreatedOn,
        #DateTime ModifiedOn,
        int CollectionCount,
        int SubGroupCount,
        int GalleryCount,
        int PhotoCount,
        #int[] ParentGroups,
        #GroupElement[] Elements,
        #string PageUrl          // new in version v1.1
    }
    """

    def _addPhotoSet(self, ps, updateChildren=False, fullyLoaded=False):
        try:
            p = PhotoSet.objects.get(Id=ps.Id)
        except PhotoSet.DoesNotExist:
            p = PhotoSet(Id=ps.Id, Owner=self.Owner)
        if updateChildren:
            p.update(psResponse=ps, 
                     updateChildren=updateChildren,
                     fullyLoaded=fullyLoaded)
        #try:
            #self.PhotoSetElements.get(Id=p.Id)
        #except PhotoSet.DoesNotExist:
        self.PhotoSetElements.add(p)
            
    def _addGroup(self, gp, updateChildren=False, fullyLoaded=False):
        try:
            g = Group.objects.get(Id=gp.Id)
        except Group.DoesNotExist:
            g = Group(Id=gp.Id, Owner=self.Owner)
        if updateChildren:
            g.update(groupResponse=gp, updateChildren=updateChildren,
                     fullyLoaded=fullyLoaded)
        #try:
            #self.GroupElements.get(Id=g.Id)
        #except Group.DoesNotExist:
        self.GroupElements.add(g)
            
    def update(self, groupResponse=None, updateChildren=False, 
               fullyLoaded=False):
        """Updates a group from Zenfolio
        
        groupResponse: preloaded response data from Zen
        fullyLoaded: whether groupResponse contains loaded photos (via
            LoadPhoto or LoadPhotoset)
        updateChildren: whether to recurse and load data for children as well
        """
        # Gets new info
        g = groupResponse
        zc = self.Owner.getConnection()
        if g is None:
            g = zc.LoadGroup(self.Id)
        assert g.Id == self.Id
        synckwds = self.__dict__.keys()
        
        #synckwds.remove('Owner_id')
        
        #synckwds.pop('ParentGroups_id')
        #synckwds.pop('GroupElements_id')
        #synckwds.pop('PhotoSetElements_id')  
        
        # The rest
        self._sync(synckwds, g)
        
        # Updates owner
        if self.Owner is None or self.Owner.LoginName != g.Owner:
            try:        
                owner=User.objects.get(LoginName=g.Owner)
            except User.DoesNotExist:
                owner=User(LoginName=g.Owner)
                owner.save()
            self.Owner = owner
            
        # Updates elements
        groups = [gp for gp in g.Elements if isinstance(gp, zenapi.snapshots.Group)]
        psets = [ps for ps in g.Elements if isinstance(ps, zenapi.snapshots.PhotoSet)]
        if not fullyLoaded and updateChildren: 
            # Even if not fullyLoaded, we may have group info from LoadHierarchy
            groups = zc.map(zc.LoadGroup, groups)
            psets = zc.map(zc.LoadPhotoSet, psets)
        if len(groups):
            [self._addGroup(gp, 
                            updateChildren=updateChildren,
                            fullyLoaded=fullyLoaded) for gp in groups]
        if len(psets):
            [self._addPhotoSet(ps,
                               updateChildren=updateChildren,
                               fullyLoaded=fullyLoaded) for ps in psets]
        
        for ps in self.PhotoSetElements.exclude(Id__in=[p.Id for p in psets]):
            ps.delete()
        for g in self.GroupElements.exclude(Id__in=[g.Id for g in groups]):
            g.delete()
            
        tp = g.TitlePhoto
        #synckwds.remove('TitlePhoto')
        try:
            if tp is None:
                raise Photo.DoesNotExist
            self.TitlePhoto=Photo.objects.get(Id=tp.Id)
        except Photo.DoesNotExist:
            if self.PhotoSetElements.count():
                ps=self.PhotoSetElements.order_by('-Views')[0]
                self.TitlePhoto = ps.TitlePhoto
            elif self.GroupElements.count():
                childids = [g.TitlePhoto.Id for g in self.GroupElements.all() 
                            if not g.TitlePhoto is None]
                ps = Photo.objects.filter(Id__in=childids)
                ps.order_by('-Views')
                self.TitlePhoto = ps[0]
                
            
        if self.GroupElements.count() == 0 \
           and self.PhotoSetElements.count()==1 \
           and self.PhotoSetElements.all()[0].Title == self.Title:
            self.FlattenMe = True
        else:
            self.FlattenMe = False
            
        self.save()
        
class PhotoSet(GroupElement):
    """Collection of photos"""
    PhotoSetTypes=Enum(Gallery=0, Collection=1) # not fully working yet
    Owner = models.ForeignKey(User, **setByZen)
    Type = models.IntegerField(choices=PhotoSetTypes.choices, **setByZen) # Enum will be gallery or collection
    Views = models.IntegerField(default=0, **setByZen)
    # API says in PhotoSet but Groups have it too - but not accessable!!

    """
    PhotoSet : GroupElement
    {
        #string Caption,
        #DateTime CreatedOn,
        #DateTime ModifiedOn,
        int PhotoCount,
        long PhotoBytes,
        int Views,
        #PhotoSetType Type,
        int FeaturedIndex,
        #Photo TitlePhoto,
        bool IsRandomTitlePhoto,
        int[] ParentGroups,
        #Photo[] Photos,
        string[] Keywords,
        int[] Categories,
        string UploadUrl,
        string PageUrl                  // new in version 1.1
    }
    """
    
        
    def update(self, psResponse=None, updateChildren=False, fullyLoaded=False):
        ps = None # Must load photos = psResponse
        zc = self.Owner.getConnection()
        if ps is None:
            ps = zc.LoadPhotoSet(self.Id)
        assert self.Id == ps.Id
        synckwds = self.__dict__.keys()
        #synckwds.pop('ParentGroups_id')
        #synckwds.pop('Keywords_id')
        #synckwds.pop('Categories_id')
        
        #synckwds.pop('Photos_id')
        synckwds.remove('Type')
        self.Type = self.PhotoSetTypes(ps.Type)
            
        # The rest
        self._sync(synckwds, ps)

        if self.Owner is None or self.Owner.LoginName != ps.Owner:
            try:
                owner=User.objects.get(LoginName=ps.Owner)
            except User.DoesNotExist:
                owner=User(LoginName=ps.Owner)
                owner.save()
            self.Owner = owner
            
        if len(ps.Photos):
            if updateChildren and not fullyLoaded:
                photos = zc.map(zc.LoadPhoto, ps.Photos)
            else:
                photos = ps.Photos
            [self._addPhoto(p, updateChildren=updateChildren) for p in photos]
            
        # Remove unfound photos
        for p in self.Photos.exclude(Id__in=[p.Id for p in photos]):
            p.delete()
            
        tp = ps.TitlePhoto
        #synckwds.remove('TitlePhoto')
        try:
            if tp is None:
                raise Photo.DoesNotExist
            self.TitlePhoto=Photo.objects.get(Id=tp.Id)
        except Photo.DoesNotExist:
                
            if self.Photos.count():
                ps=self.Photos.order_by('-Views')[0]
                self.TitlePhoto = ps
                
        self.save()
    
    def _addPhoto(self, photo, updateChildren=False):
        try:
            p = Photo.objects.get(Id=photo.Id)
        except Photo.DoesNotExist:
            p = Photo(Id=photo.Id, Owner=self.Owner)
        if updateChildren:
            p.update(photoResponse=photo, gallery=self)
        #try:
        #self.Photos.get(Id=p.Id)
        #except Photo.DoesNotExist:
        self.Photos.add(p)
   
    def adminthumb(self):
        if self.TitlePhoto:
            return self.TitlePhoto.adminthumb()
        return ''
    adminthumb.allow_tags=True
    
class Photo(GalleryElement):
    FileName = models.CharField(max_length=100, **setByZen)
    Height = models.IntegerField(**setByZen)
    Width = models.IntegerField(**setByZen)
    #Sequence = models.IntegerField(**setByZen) # Unclear what this is
    UploadedOn = models.DateTimeField(**setByZen)
    TakenOn = models.DateTimeField(**setByZen)
    Views = models.IntegerField(default=0, **setByZen)
    Gallery = models.ForeignKey(PhotoSet, related_name='Photos', **setByZen)
    
    Owner = models.ForeignKey(User, **setByZen)
    OriginalUrl = models.URLField(**setByZen)
    UrlCore = models.URLField(**setByZen)
    
    ImageSize = Enum(Original = None,
                     
    
                     ThumbRegular = 0,
                     ThumbSquare = 1,
                     ThumbLarge = 10,
                     ThumbXL = 11, # Not in API, but on site
                     ImSmall = 2,
                     ImMed = 3,
                     ImLarge = 4,
                     ImXLarge = 5,
    
                     ProfileLarge = 50,
                     ProfileSmall = 51,
                     ProfileRegular = 52,
                     )
    
    class Meta:
        ordering = ['TakenOn', 'FileName']
        
    def imageUrl(self, size=None):
        """Calculates the url to any of the resized versions
        See: http://www.zenfolio.com/zf/help/api/guide/download
        Could add port and seq # here, ignoring for now
        """
        if size is None:
            return self.OriginalUrl
        return "http://www.zenfolio.com%s-%s.jpg"%(self.UrlCore, size)
    
    @property
    def thumb_reg(self):
        return self.imageUrl(size=Photo.ImageSize.ThumbRegular)
    @property
    def thumb_lrg(self):
        return self.imageUrl(size=Photo.ImageSize.ThumbLarge)
    @property
    def thumb_xl(self):
        return self.imageUrl(size=Photo.ImageSize.ThumbXL)
    @property
    def thumb_sqr(self):
        return self.imageUrl(size=Photo.ImageSize.ThumbSquare)
    @property
    def img_sm(self):
        return self.imageUrl(size=Photo.ImageSize.ImSmall)
    @property
    def img_med(self):
        return self.imageUrl(size=Photo.ImageSize.ImMed)
    @property
    def img_lrg(self):
        return self.imageUrl(size=Photo.ImageSize.ImLarge)
    @property
    def img_xl(self):
        return self.imageUrl(size=Photo.ImageSize.ImXLarge)
    @property
    def img(self):
        return self.imageUrl()
    
    """Photo
    {
        #int Id,
        #uint Width,
        #uint Height,
        #string Sequence,
        AccessDescriptor AccessDescriptor,
        #string Title,
        #string Caption,
        #string FileName,
        #DateTime UploadedOn,
        #DateTime TakenOn,
        #string Owner,
        #int Gallery,
        int Views,
        int Size,
        string[] Keywords,
        int[] Categories,
        long PricingKey,
        string MimeType,
        #string OriginalUrl,
        #string UrlCore,
        string Copyright,
        PhotoRotation Rotation,
        byte[] FileHash,
        #string PageUrl              // new in version 1.1
    }
    """
    
    def __unicode__(self):
        return self.FileName
    
    def update(self, photoResponse=None, gallery=None):
        p=photoResponse
        if p is None:
            p = self.Owner.getConnection().LoadPhoto(self.Id)
        assert p.Id == self.Id
        synckwds = self.__dict__.keys()
        #synckwds.remove('Categories_id')
        #synckwds.pop('Keywords_id')
        #synckwds.pop('Gallery_id')
        #synckwds.remove('Sequence')
        #self.Sequence=int(p.Sequence) # dunno why this is a string
        self._sync(synckwds, p)
        
        if self.Owner is None or self.Owner.LoginName != p.Owner:
            try:
                owner=User.objects.get(LoginName=p.Owner)
            except User.DoesNotExist:
                owner=User(LoginName=p.Owner)
                owner.save()
            self.Owner = owner
        
        # Note that p.Gallery is int, not object
        if self.Gallery is None or self.Gallery.Id != p.Gallery:
            try:
                if gallery is None:
                    gallery=PhotoSet.objects.get(Id=p.Gallery)
                if gallery.Id == p.Gallery:
                    self.Gallery=gallery # Else it's a collection
                    
            except PhotoSet.DoesNotExist:
                raise NotImplementedError()# Updates currently only go downwards,
        #whereas this would have to go up the tree then back down
            
        self.save()
        
    def adminthumb(self):
        return '<a href="%s"><img src="%s"></a>'%(self.imageUrl(3),
                                                  self.imageUrl(1))
    adminthumb.allow_tags=True
    
    def ancestry(self):
        return self.Gallery.ancestry() + [self.Gallery]
