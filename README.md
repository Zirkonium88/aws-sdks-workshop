# AWS Software Development Kits (SDKs) - Wie fange ich bloß an?

Mein Chef mag es agil: Er definiert für mich diese Userstory:

```Markdown
Ich als Software Developer muss einen hochverfügbaren Speicher in AWS (Amazon Web Services) bereitstellen, um Dateien für meine Anwendung persistent zu speichern.
```

## Was muss ich tun?

Meine Anwendung braucht einen Dateispeicher in `AWS`. Welcher Service in AWS eignet sich dazu? `Antwort: Entweder Amazon Simple Storage Service (S3) oder aber das Elastic Filesystem (EFS)`.

Mist, wie wähle ich aus?

## Was ist die funktionale Anforderungen an de Dateispeicher?

Mein Chef beantwortet die Frage so:

```Markdown
Naja, eigentlich möchte mich nicht um Netzwerke kümmern müssen. Für's Patching sind wir in der Cloud. Der Speicher muss perfomant sein, aber keine Datenbank ersetzen.
```

## Entscheidung gefallen: Amazon S3

Okay, nach einer Recherche [hier](https://aws.amazon.com/s3/?nc1=h_ls) (ich habe irgendwie das Gefüphl, dass die englische Doku bei AWS besser ist ...), scheint S3 `serverless` sein - also einen ziemlich hohen Automatisierungsgrad durch AWS zu haben.

Was brauche ich? In S3 scheint die Untereinheit `Bucket` zu heißen. Mein Chef hat zwar nichts von verschlüsselung erzählt, dass kann der Service aber sowohl auf Platte als auch im Transport. Im PoC machen wir es erstaml ohne (hinther ändern wir es dann ...).

## Klicken ist out, wie kann ich etwas programmieren?

Für mich und meinen Chef soll alles in `AWS` direkt als Code abgelegt sein. Dieser `Bucket` soll daher mit einer Skriptsprache programmiert werden.

Das ist kein Problem, weil `AWS` ein HTTPS-Universum oder eine riesiger API ist, mit der man alles programmieren kann - zumindest mit den SDKs. Ein Kumpel hat mal erzählt, dass es in CloudFormation nicht so sein soll. Naja egal.

## Woher bekomme ich den Zugang?

Am einfachsten gehts üüber den [IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)
Dann installiert amn sich die [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
Schließlich legt man sich ein Profil mit `aws configure --profile myaws` mit Credentials aus de, IAM User an.

## Den Fortgang der Geschichte für Python ...

... findest du [hier](python/README.md)

## Den Fortgang der Geschichte für Go ...

... findest du [hier](go/README.md)

## Den Fortgang der Geschichte für TypeScript ...

... findest du [hier](typescript/README.md)