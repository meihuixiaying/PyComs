#!/usr/bin/python 
# -*- coding: utf-8 -*-

from src.models import Project
from src.misc.decorator import transfer2jsonwithoutset , slicejson
from sqlalchemy import desc
from src.misc.exts import db
from flask import request


class ProjectBusiness(object):
    @classmethod
    def _query(cls):
        return Project.query \
            .add_columns(
            Project.id.label('id'),
            Project.name.label('name'),
            Project.description.label('description'),
            Project.status.label('status'),
            Project.logo.label('logo'),
            Project.weight.label('weight'),
        )

    @classmethod
    @transfer2jsonwithoutset('?id|!name|!description|!status|!weight|!logo')
    def query_all(cls, limit, offset):
        return cls._query().filter(Project.status == Project.ACTIVE).order_by(desc(Project.weight)).order_by(
            Project.id).all()

    @classmethod
    @transfer2jsonwithoutset('?id|!name|!description|!status|!weight|!logo')
    def query_by_id(cls, id):
        return cls._query().filter(Project.id == id, Project.status == Project.ACTIVE).order_by(
            desc(Project.weight)).all()

    @classmethod
    def add(cls, name, description, logo):
        try:
            p = Project(
                name=name,
                description=description,
                logo=logo,
            )
            db.session.add(p)
            db.session.commit()
            return 0, None
        except Exception as e:
            return 102, str(e)

    @classmethod
    def update(cls, id, name, description, weight, logo):
        project = Project.query.get(id)
        if project.status == Project.ACTIVE:
            try:
                project.name = name
                project.description = description
                project.weight = weight
                project.logo = logo
            except Exception as e:
                db.session.rollback()
                return 102, str(e)

    @classmethod
    def delete(cls, id):
        project = Project.query.get(id)
        project.status = Project.DISABLE
        db.session.add(project)
        db.session.commit()
        return 0

