﻿using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

#nullable disable

namespace webapi
{
    public partial class ToxicityContext : DbContext
    {
        public ToxicityContext()
        {
        }

        public ToxicityContext(DbContextOptions<ToxicityContext> options)
            : base(options)
        {
        }

        public virtual DbSet<FlywaySchemaHistory> FlywaySchemaHistory { get; set; }
        public virtual DbSet<ToxicityAnnotations> ToxicityAnnotations { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.HasAnnotation("Relational:Collation", "en_US.utf8");

            modelBuilder.Entity<FlywaySchemaHistory>(entity =>
            {
                entity.HasKey(e => e.InstalledRank)
                    .HasName("flyway_schema_history_pk");

                entity.ToTable("flyway_schema_history");

                entity.HasIndex(e => e.Success, "flyway_schema_history_s_idx");

                entity.Property(e => e.InstalledRank)
                    .ValueGeneratedNever()
                    .HasColumnName("installed_rank");

                entity.Property(e => e.Checksum).HasColumnName("checksum");

                entity.Property(e => e.Description)
                    .IsRequired()
                    .HasMaxLength(200)
                    .HasColumnName("description");

                entity.Property(e => e.ExecutionTime).HasColumnName("execution_time");

                entity.Property(e => e.InstalledBy)
                    .IsRequired()
                    .HasMaxLength(100)
                    .HasColumnName("installed_by");

                entity.Property(e => e.InstalledOn)
                    .HasColumnName("installed_on")
                    .HasDefaultValueSql("now()");

                entity.Property(e => e.Script)
                    .IsRequired()
                    .HasMaxLength(1000)
                    .HasColumnName("script");

                entity.Property(e => e.Success).HasColumnName("success");

                entity.Property(e => e.Type)
                    .IsRequired()
                    .HasMaxLength(20)
                    .HasColumnName("type");

                entity.Property(e => e.Version)
                    .HasMaxLength(50)
                    .HasColumnName("version");
            });

            modelBuilder.Entity<ToxicityAnnotations>(entity =>
            {
                entity.HasNoKey();

                entity.ToTable("toxicity_annotations");

                entity.Property(e => e.RevId).HasColumnName("rev_id");

                entity.Property(e => e.Toxicity).HasColumnName("toxicity");

                entity.Property(e => e.ToxicityScore).HasColumnName("toxicity_score");

                entity.Property(e => e.WorkerId).HasColumnName("worker_id");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
