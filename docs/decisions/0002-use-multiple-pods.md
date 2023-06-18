# Use multiple Pods

---

- status: accepted
- date: 2023-06-18
- deciders:
  - johannes.bornhold.extern@univention.de

---

## Context

The two containers `ldap-server` and `ldap-notifier` are exchanging through an
API which is based on a shared filesystem.

This can be modeled in Kubernetes in the following two approaches:

1. Run both *Containers* in the same *Pod*. This way they share some resources
   and are automatically running on the same *Node*. This pattern is recommended
   for closely entangled applications.

2. Run each *Container* in its own *Pod*. This way they can be scheduled on
   different *Nodes* potentially.

Volumes have an access mode which describes their capabilities, e.g.
`ReadWriteOnce` or `ReadWriteMany`. The suffix "Once" or "Many" is related to
the aspect if this volume can be used only on one *Node* or across multiple
*Nodes*.


## Decision

The containers will be configured as two distinct *Pods*.


## Consequences

Using two *Pods* does mean that they can be scheduled across multiple *Nodes*
and share a volume in a networked way. This may have implications regarding the
performance and in the worst case regarding the functionality if certain
filesystem features are not giving the same guarantees like a local file system.

The decision should be easy to reverse in the future by changes in the Helm
templates without a need to change the implementation.


## More information

Kubernetes API reference documentation:

- `Pod` - https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/

- `PersistentVolumeClaim` - https://kubernetes.io/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-claim-v1/
