from database import db
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
import ipaddress
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime


class Host(db.Model):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String, unique=True, nullable=False, index=True)
    ipv4 = Column(String, nullable=False, index=True)
    ipv6 = Column(String, index=True)
    cidr = Column(Integer)
    deleted = Column(Boolean, default=False)
    ports = relationship("Port", back_populates="host")
    tags = relationship("HostTag", back_populates="host")

    @validates("ipv4", "ipv6")
    def validate_ip(self, key, address):
        if address:
            try:
                ip_obj = ipaddress.ip_address(address)
                if (key == "ipv4" and ip_obj.version != 4) or (
                    key == "ipv6" and ip_obj.version != 6
                ):
                    raise ValueError(f"Invalid {key} address: {address}")
                return str(ip_obj)
            except ValueError:
                raise ValueError(f"Invalid {key} address: {address}")
        return address


class Tag(db.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, unique=True, nullable=False, index=True)
    deleted = Column(Boolean, default=False)
    hosts = relationship("HostTag", back_populates="tag")


class HostTag(db.Model):
    __tablename__ = "host_tags"
    host_id = Column(Integer, ForeignKey("hosts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    host = relationship("Host", back_populates="tags")
    tag = relationship("Tag", back_populates="hosts")


class Port(db.Model):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey("hosts.id"))
    port_number = Column(Integer, nullable=False)
    deleted = Column(Boolean, default=False)
    host = relationship("Host", back_populates="ports")


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    action_type = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = Column(String, nullable=False)


class Statistics(db.Model):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stat_key = Column(String, nullable=False, index=True)
    stat_value = Column(Integer, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DiscoveredDevice(db.Model):
    __tablename__ = "discovered_devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mac_address = Column(String, nullable=False, index=True)
    ipv4 = Column(String, nullable=False, index=True)
    ipv6 = Column(String, index=True)
    hostname = Column(String, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False)
    vendor = Column(String)
    ignore = Column(Boolean, default=False)

    @validates("ipv4", "ipv6")
    def validate_ip(self, key, address):
        if address:
            try:
                ip_obj = ipaddress.ip_address(address)
                if (key == "ipv4" and ip_obj.version != 4) or (
                    key == "ipv6" and ip_obj.version != 6
                ):
                    raise ValueError(f"Invalid {key} address: {address}")
                return str(ip_obj)
            except ValueError:
                raise ValueError(f"Invalid {key} address: {address}")
        return address
