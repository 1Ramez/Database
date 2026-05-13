USE master
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'VetClinic')
    CREATE DATABASE VetClinic
GO

USE VetClinic
GO

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('CLINICAL_NOTE') and o.name = 'FK_CLINICAL_RECORD_VETERINA')
alter table CLINICAL_NOTE
   drop constraint FK_CLINICAL_RECORD_VETERINA
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('PET') and o.name = 'FK_PET_OWNS_OWNER')
alter table PET
   drop constraint FK_PET_OWNS_OWNER
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('VACCINATIONRECORD') and o.name = 'FK_VACCINAT_INCLUDE_CLINICAL')
alter table VACCINATIONRECORD
   drop constraint FK_VACCINAT_INCLUDE_CLINICAL
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('VACCINATIONRECORD') and o.name = 'FK_VACCINAT_REFERS_VACCINE')
alter table VACCINATIONRECORD
   drop constraint FK_VACCINAT_REFERS_VACCINE
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('VIST') and o.name = 'FK_VIST_HOST_CLINIC')
alter table VIST
   drop constraint FK_VIST_HOST_CLINIC
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('VIST') and o.name = 'FK_VIST_VIST_PET')
alter table VIST
   drop constraint FK_VIST_VIST_PET
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('VIST') and o.name = 'FK_VIST_WITH_VETERINA')
alter table VIST
   drop constraint FK_VIST_WITH_VETERINA
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('WORKSAT') and o.name = 'FK_WORKSAT_WORKSAT_VETERINA')
alter table WORKSAT
   drop constraint FK_WORKSAT_WORKSAT_VETERINA
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('WORKSAT') and o.name = 'FK_WORKSAT_WORKSAT2_CLINIC')
alter table WORKSAT
   drop constraint FK_WORKSAT_WORKSAT2_CLINIC
go

if exists (select 1
            from  sysobjects
           where  id = object_id('CLINIC')
            and   type = 'U')
   drop table CLINIC
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('CLINICAL_NOTE')
            and   name  = 'RECORD_FK'
            and   indid > 0
            and   indid < 255)
   drop index CLINICAL_NOTE.RECORD_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('CLINICAL_NOTE')
            and   type = 'U')
   drop table CLINICAL_NOTE
go

if exists (select 1
            from  sysobjects
           where  id = object_id('OWNER')
            and   type = 'U')
   drop table OWNER
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('PET')
            and   name  = 'OWNS_FK'
            and   indid > 0
            and   indid < 255)
   drop index PET.OWNS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('PET')
            and   type = 'U')
   drop table PET
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('VACCINATIONRECORD')
            and   name  = 'REFERS_FK'
            and   indid > 0
            and   indid < 255)
   drop index VACCINATIONRECORD.REFERS_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('VACCINATIONRECORD')
            and   name  = 'INCLUDE_FK'
            and   indid > 0
            and   indid < 255)
   drop index VACCINATIONRECORD.INCLUDE_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('VACCINATIONRECORD')
            and   type = 'U')
   drop table VACCINATIONRECORD
go

if exists (select 1
            from  sysobjects
           where  id = object_id('VACCINE')
            and   type = 'U')
   drop table VACCINE
go

if exists (select 1
            from  sysobjects
           where  id = object_id('VETERINARIAN')
            and   type = 'U')
   drop table VETERINARIAN
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('VIST')
            and   name  = 'WITH_FK'
            and   indid > 0
            and   indid < 255)
   drop index VIST.WITH_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('VIST')
            and   name  = 'HOST_FK'
            and   indid > 0
            and   indid < 255)
   drop index VIST.HOST_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('VIST')
            and   name  = 'VIST_FK'
            and   indid > 0
            and   indid < 255)
   drop index VIST.VIST_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('VIST')
            and   type = 'U')
   drop table VIST
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('WORKSAT')
            and   name  = 'WORKSAT2_FK'
            and   indid > 0
            and   indid < 255)
   drop index WORKSAT.WORKSAT2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('WORKSAT')
            and   name  = 'WORKSAT_FK'
            and   indid > 0
            and   indid < 255)
   drop index WORKSAT.WORKSAT_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('WORKSAT')
            and   type = 'U')
   drop table WORKSAT
go

/*==============================================================*/
/* Table: CLINIC                                                */
/*==============================================================*/
create table CLINIC (
   CLINICID             INT IDENTITY(1,1)    NOT NULL,
   LOCATION             varchar(1024)        null,
   C_NAME               varchar(1024)        not null,
   EMERGENCTDCALILITIES varchar(1024)        null,
   constraint PK_CLINIC primary key nonclustered (CLINICID)
)
go

/*==============================================================*/
/* Table: CLINICAL_NOTE                                         */
/*==============================================================*/
create table CLINICAL_NOTE (
   NOTEID               INT IDENTITY(1,1)    NOT NULL,
   VETID                int                  null,
   P_WEIGHT             float                null,
   CREATEDDATE          datetime             null,
   NOTES                varchar(1024)        null,
   constraint PK_CLINICAL_NOTE primary key nonclustered (NOTEID)
)
go

/*==============================================================*/
/* Index: RECORD_FK                                             */
/*==============================================================*/
create index RECORD_FK on CLINICAL_NOTE (
VETID ASC
)
go

/*==============================================================*/
/* Table: OWNER                                                 */
/*==============================================================*/
create table OWNER (
   OWNERID              INT IDENTITY(1,1)    NOT NULL,
   O_NAME               VARCHAR(1024)        NOT NULL,
   BILLINGADDRESS       VARCHAR(1024)        NULL,
   EMERGENCYCONTACT     VARCHAR(1024)        NULL,
   PHONE                NUMERIC              NULL,
   CONSTRAINT PK_OWNER PRIMARY KEY NONCLUSTERED (OWNERID)
)
go

/*==============================================================*/
/* Table: PET                                                   */
/*==============================================================*/
create table PET (
   PETID                INT IDENTITY(1,1)    NOT NULL,
   OWNERID              int                  null,
   P_NAME               varchar(1024)        not null,
   BREED                varchar(1024)        not null,
   DATEOFBIRTH          datetime             not null,
   GENDER               varchar(1024)        not null,
   SPECIE               varchar(1024)        not null,
   constraint PK_PET primary key nonclustered (PETID)
)
go

/*==============================================================*/
/* Index: OWNS_FK                                               */
/*==============================================================*/
create index OWNS_FK on PET (
OWNERID ASC
)
go

/*==============================================================*/
/* Table: VACCINATIONRECORD                                     */
/*==============================================================*/
create table VACCINATIONRECORD (
   BATCHNUM             numeric              null,
   DATENEXTBOOSTER      datetime             null,
   VACCINETYPE          varchar(1024)        null,
   RECORDID             INT IDENTITY(1,1)    NOT NULL,
   NOTEID               int                  null,
   VACCINEID            int                  null,
   constraint PK_VACCINATIONRECORD primary key nonclustered (RECORDID)
)
go

/*==============================================================*/
/* Index: INCLUDE_FK                                            */
/*==============================================================*/
create index INCLUDE_FK on VACCINATIONRECORD (
NOTEID ASC
)
go

/*==============================================================*/
/* Index: REFERS_FK                                             */
/*==============================================================*/
create index REFERS_FK on VACCINATIONRECORD (
VACCINEID ASC
)
go

/*==============================================================*/
/* Table: VACCINE                                               */
/*==============================================================*/
create table VACCINE (
   VACCINENAME          varchar(1024)        not null,
   VACCINEID            INT IDENTITY(1,1)    NOT NULL,
   constraint PK_VACCINE primary key nonclustered (VACCINEID)
)
go

/*==============================================================*/
/* Table: VETERINARIAN                                          */
/*==============================================================*/
create table VETERINARIAN (
   VETID                INT IDENTITY(1,1)    NOT NULL,
   V_NAME               varchar(1024)        not null,
   PHONE                numeric              null,
   EXPERTISE            varchar(1024)        null,
   constraint PK_VETERINARIAN primary key nonclustered (VETID)
)
go

/*==============================================================*/
/* Table: VIST                                                  */
/*==============================================================*/
create table VIST (
   VISTID               INT IDENTITY(1,1)    NOT NULL,
   CLINICID             int                  null,
   PETID                int                  null,
   VETID                int                  null,
   VISTDATE             datetime             not null,
   REASON               varchar(1024)        not null,
   constraint PK_VIST primary key nonclustered (VISTID)
)
go

/*==============================================================*/
/* Index: VIST_FK                                               */
/*==============================================================*/
create index VIST_FK on VIST (
PETID ASC
)
go

/*==============================================================*/
/* Index: HOST_FK                                               */
/*==============================================================*/
create index HOST_FK on VIST (
CLINICID ASC
)
go

/*==============================================================*/
/* Index: WITH_FK                                               */
/*==============================================================*/
create index WITH_FK on VIST (
VETID ASC
)
go

/*==============================================================*/
/* Table: WORKSAT                                               */
/*==============================================================*/
create table WORKSAT (
   VETID                int                  not null,
   CLINICID             int                  not null,
   constraint PK_WORKSAT primary key (VETID, CLINICID)
)
go

/*==============================================================*/
/* Index: WORKSAT_FK                                            */
/*==============================================================*/
create index WORKSAT_FK on WORKSAT (
VETID ASC
)
go

/*==============================================================*/
/* Index: WORKSAT2_FK                                           */
/*==============================================================*/
create index WORKSAT2_FK on WORKSAT (
CLINICID ASC
)
go

alter table CLINICAL_NOTE
   add constraint FK_CLINICAL_RECORD_VETERINA foreign key (VETID)
      references VETERINARIAN (VETID)
go

alter table PET
   add constraint FK_PET_OWNS_OWNER foreign key (OWNERID)
      references OWNER (OWNERID)
go

alter table VACCINATIONRECORD
   add constraint FK_VACCINAT_INCLUDE_CLINICAL foreign key (NOTEID)
      references CLINICAL_NOTE (NOTEID)
go

alter table VACCINATIONRECORD
   add constraint FK_VACCINAT_REFERS_VACCINE foreign key (VACCINEID)
      references VACCINE (VACCINEID)
go

alter table VIST
   add constraint FK_VIST_HOST_CLINIC foreign key (CLINICID)
      references CLINIC (CLINICID)
go

alter table VIST
   add constraint FK_VIST_VIST_PET foreign key (PETID)
      references PET (PETID)
go

alter table VIST
   add constraint FK_VIST_WITH_VETERINA foreign key (VETID)
      references VETERINARIAN (VETID)
go

alter table WORKSAT
   add constraint FK_WORKSAT_WORKSAT_VETERINA foreign key (VETID)
      references VETERINARIAN (VETID)
go

alter table WORKSAT
   add constraint FK_WORKSAT_WORKSAT2_CLINIC foreign key (CLINICID)
      references CLINIC (CLINICID)
go