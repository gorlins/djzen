from django.db import models
import zenapi

# Create your models here.

setByZen = dict(editable=False, null=True, blank=True)

# Models
class User(models.Model):
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
    #RootGroup = models.ForeignKey('Group', **setByZen)

    RootGroup = models.IntegerField(**setByZen) # Id of root group
    
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
    
    def update(self):
        ro = self.getConnection().LoadPublicProfile()
        for k in self.__dict__:
            try:
                v = ro._dict[k]
                if hasattr(v, 'Id'):
                    v = v.Id
                elif hasattr(v, 'Value'):
                    v = v.Value
                setattr(self, k, v)
            except KeyError:
                pass
    
    def getConnection(self):
        return zenapi.ZenConnection(username=self.LoginName)
    
class GroupElement(models.Model):
    """Abstract base for photosets and groups"""
    GroupIndex = models.IntegerField(primary_key=True, db_index=True, **setByZen)
    Title = models.CharField(max_length=60, **setByZen)
    Owner = models.ForeignKey(User, **setByZen)
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
        
class Group(GroupElement):
    """Folder-like collection of groups and photosets"""
    Caption = models.CharField(max_length=100, **setByZen)
    CreatedOn = models.DateTimeField(**setByZen)
    ModifiedOn = models.DateTimeField(**setByZen)
    
    #ParentGroups = models.ManyToManyField('self', related_name='GroupElements',
                                          #symmetrical=False) # in GroupElements
    #GroupElements = models.ManyToManyField(GroupElement)
    PageUrl = models.URLField()
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
    
class PhotoSet(GroupElement):
    """Collection of photos"""
    Caption = models.CharField(max_length=100, **setByZen)
    CreatedOn = models.DateTimeField(**setByZen)
    ModifiedOn = models.DateTimeField(**setByZen)
    Type = models.IntegerField(**setByZen) # Enum will be gallery or collection

    TitlePhoto = models.ForeignKey('Photo', **setByZen)
    PageUrl = models.URLField(**setByZen)
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
    
class Photo(models.Model):
    Id = models.IntegerField(primary_key=True, db_index=True, **setByZen)
    
    Title = models.CharField(max_length=100, **setByZen)
    Caption = models.CharField(max_length=100, **setByZen)
    FileName = models.CharField(max_length=100, **setByZen)
    
    UploadedOn = models.DateTimeField(**setByZen)
    TakenOn = models.DateTimeField(**setByZen)
    
    Owner = models.ForeignKey(User, **setByZen)
    Gallery = models.ForeignKey(PhotoSet, related_name='Photos', **setByZen)
    
    OriginalUrl = models.URLField(**setByZen)
    UrlCore = models.URLField(**setByZen)
    PageUrl = models.URLField(**setByZen)
    """Photo
    {
        #int Id,
        uint Width,
        uint Height,
        string Sequence,
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